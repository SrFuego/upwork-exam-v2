import json
from datetime import datetime, timedelta
from typing import Annotated

from jose import jwt, JWTError
from sqlmodel import Session

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ...application.exceptions import (
    CREDENTIALS_EXCEPTION,
    INCORRECT_USERNAME_OR_PASSWORD_EXCEPTION,
)
from ...infrastructure.schemas.user import TokenData
from ...infrastructure.repository.db import get_user_by_username
from ...infrastructure.security import verify_password
from ...infrastructure.repository.sqlite3 import get_session

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "67b3d7fcecc21582d31ac273de5407552fda4b58133e9490a4f81906cb34f6a5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login/")


def authenticate_user(
    session: Session = Depends(get_session),
    username: str = "",
    password: str = "",
):
    if not username:
        raise CREDENTIALS_EXCEPTION
    if not password:
        raise CREDENTIALS_EXCEPTION
    user = get_user_by_username(session, username)
    if not user:
        raise INCORRECT_USERNAME_OR_PASSWORD_EXCEPTION
    if not verify_password(password, user.hashed_password):
        raise INCORRECT_USERNAME_OR_PASSWORD_EXCEPTION
    access_token = create_access_token(
        data={
            "username": user.username,
        }
    )
    return access_token


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    expire = json.dumps(expire, default=str)
    to_encode.update({"expire": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}


async def get_current_user(
    *,
    session: Session = Depends(get_session),
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if not username:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = get_user_by_username(session, token_data.username)
    if not user:
        raise CREDENTIALS_EXCEPTION
    return user
