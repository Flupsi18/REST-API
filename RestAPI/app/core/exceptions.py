from typing import Any
from fastapi import HTTPException, status


class AuthFailedException(HTTPException):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail if detail else "Authenticate failed",
            headers={"WWW-Authenticate": "Bearer"}
        )
