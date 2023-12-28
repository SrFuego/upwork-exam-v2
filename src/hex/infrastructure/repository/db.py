from sqlmodel import Session, select

from ..schemas.profile import ProfileIn
from ..schemas.user import UserIn
from .tables import User, Profile


def create_user_in_db(
    session: Session,
    user_in: UserIn,
    hashed_password: str,
) -> User:
    user = User(
        **user_in.model_dump(),
        hashed_password=hashed_password,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user


def get_user_by_username(
    session: Session,
    username: str,
) -> User:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    user = results.first()
    if not user:
        return False
    return user


def get_user_by_id(
    session: Session,
    user_id: int,
) -> User:
    statement = select(User).where(User.id == user_id)
    results = session.exec(statement)
    user = results.first()
    if not user:
        return False
    return user


def delete_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    user = results.first()
    session.delete(user)
    session.commit()
    session.close()
    return results


def create_profile_in_db(
    session: Session,
    user_id: int,
    profile_in: ProfileIn,
) -> Profile:
    profile = Profile(
        **profile_in.model_dump(),
        user_id=user_id,
    )
    session.add(profile)
    session.commit()
    session.refresh(profile)
    session.close()
    return profile


def get_profiles_by_user_id(session: Session, user_id: int):
    statement = select(Profile).where(Profile.user_id == user_id)
    results = session.exec(statement)
    profile = results.all()
    return profile


def get_profile_by_id(session: Session, profile_id: int) -> Profile:
    statement = select(Profile).where(Profile.id == profile_id)
    results = session.exec(statement)
    profile = results.first()
    return profile


def delete_profile_by_id(session: Session, profile_id: int):
    statement = select(Profile).where(Profile.id == profile_id)
    results = session.exec(statement)
    profile = results.first()
    session.delete(profile)
    session.commit()
    session.close()
    return results


def get_other_profiles_by_user_id(session: Session, user_id: int):
    statement = select(Profile).where(Profile.user_id != user_id)
    results = session.exec(statement)
    profile = results.all()
    return profile


def get_profiles_by_id(session: Session, profile_ids: list[str]):
    statement = select(Profile).filter(Profile.id.in_(profile_ids))
    results = session.exec(statement)
    profiles = results.all()
    return profiles
