from sqlmodel import Relationship, Field

from ...domain.models import UserBase, ProfileBase


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

    profiles: list["Profile"] = Relationship(back_populates="user")
    profile_favorites: str | None

    def favorites_list(self):
        if self.profile_favorites:
            if "," in self.profile_favorites:
                return self.profile_favorites.split(",")
            else:
                return [
                    self.profile_favorites,
                ]
        else:
            return []


class Profile(ProfileBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="profiles")
