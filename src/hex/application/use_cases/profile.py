from sqlmodel import Session

from ...infrastructure.repository.tables import Profile, User
from ...infrastructure.schemas.profile import (
    AddToFavoritesIn,
    ProfileIn,
    ProfileOut,
)
from ...infrastructure.repository.db import (
    create_profile_in_db,
    get_user_by_id,
    get_profiles_by_user_id,
    get_profile_by_id,
    delete_profile_by_id,
    get_other_profiles_by_user_id,
)


def create_profile(
    session: Session,
    user_id: int,
    profile_in: ProfileIn,
) -> ProfileOut:
    profile = create_profile_in_db(session, user_id, profile_in)
    user = get_user_by_id(session, user_id)
    profile_out = ProfileOut(
        name=profile.name,
        description=profile.description,
        user=user,
    )
    return profile_out


def get_profiles(session: Session, user: User) -> list[Profile]:
    profiles = get_profiles_by_user_id(session, user.id)
    return [profile for profile in profiles]


def update_profile(
    session: Session,
    profile_id: int,
    profile_in: ProfileIn,
) -> ProfileOut:
    profile = get_profile_by_id(session, profile_id)
    profile.name = profile_in.name
    profile.description = profile_in.description
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return ProfileOut(
        name=profile.name,
        description=profile.description,
        user=profile.user,
    )


def delete_profile(
    session: Session,
    profile_id: int,
):
    delete_profile_by_id(session, profile_id)
    return {"response": "Profile deleted"}


def get_other_profiles(session: Session, user_id: int) -> list[Profile]:
    profiles = get_other_profiles_by_user_id(session, user_id)
    return [profile for profile in profiles]


def add_to_favorite_profiles(
    session: Session,
    user: User,
    profiles: AddToFavoritesIn,
) -> dict:
    user.profile_favorites = profiles.to_string()
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"response": "Profiles added to favorites"}
