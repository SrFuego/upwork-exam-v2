from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(unique=True)


class ProfileBase(SQLModel):
    name: str
    description: str
