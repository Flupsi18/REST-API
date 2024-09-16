from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """
    Represents a token used for authentication.

    This class defines the structure of a token, including the access token and its type.

    Attributes:
    - access_token (str): The access token for authentication.
    - token_type (str): The type of the token.
    """
    access_token: Optional[str] = None
    token_type: Optional[str] = None

    class Config:
        populate_by_name = True


class TokenData(BaseModel):
    """
    Represents data associated with a token.

    This class defines the structure of data associated with a token, such as the username.

    Attributes:
    - username (str): The username associated with the token.
    """
    name: Optional[str] = None

    class Config:
        populate_by_name = True
