from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from ...core.exceptions import AuthFailedException
from ...core.security import create_access_token, create_refresh_token, add_refresh_token_cookie
from ...database.mongodb import DataService
from ...models.token import Token

router = APIRouter()


# only **for testing** in the api docs
@router.post("/api/token",
             responses={
                 401: {
                     "description": "Unauthorized",
                     "content": {"application/json": {"example": {"detail": "Wrong username or password"}}},
                 },
                 500: {
                     "description": "Internal Server Error",
                     "content": {"application/json": {"example": {"detail": "Failed to authenticate user"}}},
                 }

             },
             status_code=status.HTTP_200_OK,
             response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response
):
    """
    ! Only for authentication with fastAPI docs !

    Authenticates a user and provides an access token.

    This endpoint accepts a username and password, authenticates the user (customer or company),
    and returns an access token if authentication is successful.

    Args:
    - form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
    - db (AsyncIOMotorClient): Asynchronous Motor client for the MongoDB database.

    Raises:
    - HTTPException(HTTP_401_UNAUTHORIZED): If authentication fails for both customer and company.
    - HTTPException(HTTP_500_INTERNAL_SERVER_ERROR): If there is a server error during authentication.

    Returns:
    - Token: The access token for the authenticated user.
    """

    customer = await DataService.authenticate_customer(form_data.username, form_data.password)

    if not customer:
        raise AuthFailedException(detail="Incorrect name or password")

    access_token = create_access_token(customer.get("_id"))
    refresh_token = create_refresh_token(customer.get("_id"))

    add_refresh_token_cookie(response, refresh_token)

    return {
        "access_token": access_token
    }
