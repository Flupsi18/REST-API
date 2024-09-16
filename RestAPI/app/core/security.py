from datetime import datetime, timedelta

import bson.errors
import hashlib
from fastapi import Response
from .config import settings
from jose import jwt, JWTError
from typing import Union, Any
from .exceptions import AuthFailedException


# Create Access Token
def create_access_token(subject: Union[int, Any], expires_delta: int = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        print(f"expire: {expire}")
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    print(f"encoded_jwt: {encoded_jwt}")
    return encoded_jwt


#  Create Refresh Token
def create_refresh_token(subject: Union[int, Any], expires_delta: int = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        print(f"expire: {expire}")
    else:
        expire = datetime.utcnow() + timedelta(settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    print(f"encoded_jwt: {encoded_jwt}")
    return encoded_jwt


# This method refreshes the current Token and creates a new access_token
def refresh_token_state(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as ex:
        print(str(ex))
        raise AuthFailedException()

    return create_access_token(payload.get("sub"))


# Add refresh Token to cookie for refreshing to access_token
def add_refresh_token_cookie(response: Response, token: str):
    response.set_cookie(
        key="refresh",
        value=token,
        httponly=True
    )


# Decode Token and check if customer id is valid
async def decode_access_token_customer(token: str, db):
    print(token)
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"DEBUG: {payload}")
        customer_id: Union[int, Any] = float(payload.get("sub"))
        if customer_id is None:
            raise AuthFailedException()
    except (ValueError, JWTError) as ex:
        print(str(ex))
        raise AuthFailedException()
    customer = await db.get_customer_by_id(customer_id) # Variabel
    if customer is None:
        raise AuthFailedException()
    return customer


# Decode Token and check if company id is valid
async def decode_access_token_company(token: str, db):
    print(token)
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"DEBUG: {payload}")
        company_id: str = payload.get("sub")
        if company_id is None:
            raise AuthFailedException()
    except JWTError as ex:
        print(str(ex))
        raise AuthFailedException()
    try:
        company = await db.get_company_by_id(str(company_id)) # Variabel
        if company is None:
            raise AuthFailedException()
        return company
    except bson.errors.InvalidId as ex:
        print(str(ex))
        raise AuthFailedException()


def get_password_hash(password: str) -> str:
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')
    # Create a hashlib object using the SHA-256 algorithm
    hasher = hashlib.sha256()
    # Hash the password
    hasher.update(password_bytes)
    # Get the hexadecimal representation of the hash
    hashed_password = hasher.hexdigest()

    return hashed_password


def verify_password(stored_hash: str, provided_password: str) -> bool:
    # Hash the provided password
    provided_hash = get_password_hash(provided_password)
    # Compare the stored hash with the provided hash
    return stored_hash == provided_hash