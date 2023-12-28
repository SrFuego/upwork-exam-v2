from sqlmodel import Session

from ...infrastructure.schemas.user import UserIn
from ...infrastructure.repository.db import (
    create_user_in_db,
    delete_user_by_username,
)
from ...infrastructure.repository.tables import User
from ...infrastructure.security import get_password_hash
from ...infrastructure.repository.validations import check_email_in_use


def create_user(session: Session, user_in: UserIn):
    check_email_in_use(session, user_in.username)
    hashed_password = get_password_hash(user_in.password)
    create_user_in_db(session, user_in, hashed_password)
    return {"response": "User created"}


def delete_user(session: Session, user: User):
    delete_user_by_username(session, user.username)
    return {"response": "User deleted"}
