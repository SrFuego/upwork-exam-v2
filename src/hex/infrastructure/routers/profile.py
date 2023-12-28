from typing import Annotated

from sqlmodel import Session

from fastapi import APIRouter, status, Depends

from ...infrastructure.schemas.profile import (
    ProfileIn,
    ProfileOut,
    UserProfilesOut,
    OtherProfilesOut,
    AddToFavoritesIn,
)
from ...application.use_cases.auth import get_current_user
from ...application.use_cases.profile import (
    create_profile,
    get_profiles,
    update_profile,
    delete_profile,
    get_other_profiles,
    add_to_favorite_profiles,
    get_favorite_profiles,
    delete_favorite_profile,
)
from ...infrastructure.repository.tables import User
from ...infrastructure.repository.sqlite3 import get_session


router = APIRouter(prefix="/profile")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProfileOut,
    tags=["profile"],
)
async def create_profile_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
    profile_in: ProfileIn,
):
    new_profile = create_profile(
        session,
        current_user.id,
        profile_in,
    )
    return new_profile


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserProfilesOut,
    tags=["profile"],
)
async def get_profile_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
):
    profiles = get_profiles(session, current_user)
    response = UserProfilesOut(user=current_user, profiles=profiles)
    return response


@router.patch(
    "/{profile_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ProfileOut,
    tags=["profile"],
)
async def update_profile_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
    profile_in: ProfileIn,
    profile_id: int,
):
    updated_profile = update_profile(session, profile_id, profile_in)
    return updated_profile


@router.delete(
    "/{profile_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["profile"],
)
async def delete_profile_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
    profile_id: int,
):
    response = delete_profile(session, profile_id)
    return response


@router.get(
    "/others/",
    status_code=status.HTTP_200_OK,
    response_model=OtherProfilesOut,
    tags=["profile"],
)
async def others_profiles_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
):
    profiles = get_other_profiles(session, current_user.id)
    response = OtherProfilesOut(profiles=profiles)
    return response


@router.post(
    "/favorites/",
    status_code=status.HTTP_201_CREATED,
    tags=["favorites"],
)
async def add_profiles_to_favorites_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
    profiles_to_add: AddToFavoritesIn,
):
    response = add_to_favorite_profiles(
        session,
        current_user,
        profiles_to_add,
    )
    return response


@router.get(
    "/favorites/",
    status_code=status.HTTP_200_OK,
    response_model=OtherProfilesOut,
    tags=["favorites"],
)
async def get_favorite_profiles_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
):
    profiles = get_favorite_profiles(session, current_user)
    return OtherProfilesOut(profiles=profiles)


@router.delete(
    "/favorites/{profile_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["favorites"],
)
async def get_favorite_profiles_endpoint(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_user)],
    profile_id: int,
):
    response = delete_favorite_profile(
        session,
        current_user,
        profile_id,
    )
    return response
