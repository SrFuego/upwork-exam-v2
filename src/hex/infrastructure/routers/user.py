from typing import Annotated

from sqlmodel import Session

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ...infrastructure.repository.tables import User
from ...application.use_cases.user import create_user, delete_user
from ...application.use_cases.auth import (
    authenticate_user,
    get_current_user,
)
from ...infrastructure.repository.sqlite3 import get_session
from ..schemas.user import UserIn, Token
from .profile import router as profile_router


router = APIRouter(prefix="/users")
router.include_router(profile_router)


@router.post(
    "/sign-up/",
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
)
async def create_user_endpoint(
    *,
    session: Session = Depends(get_session),
    user_in: UserIn,
):
    response = create_user(session, user_in)
    return response


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    tags=["auth"],
)
async def login_for_access_token_endpoint(
    *,
    session: Session = Depends(get_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    response = authenticate_user(
        session,
        form_data.username,
        form_data.password,
    )
    return response


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["user"],
)
async def delete_user_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
):
    response = delete_user(session, current_user)
    return response
