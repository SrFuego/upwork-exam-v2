from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from ...domain.models import UserBase


class UserIn(UserBase):
    username: EmailStr = Field(unique=True)
    password: str = Field(min_length=8, max_length=20)


class UserOut(UserBase):
    pass


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str
