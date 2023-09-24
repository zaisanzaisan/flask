from typing import Optional

from pydantic import BaseModel, validator

from models import User, get_session


class UserValidate(BaseModel):
    name: str

    @validator("name")
    def secure_name(cls, value):
        if len(value) > 32:
            raise ValueError("Name is too long.")
        return value


class AdvValidate(BaseModel):
    id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    owner_id: int

    @validator("owner_id")
    def secure_owner_id(cls, value):
        session = get_session()
        if len(session.query(User).where(User.id == value).all()) < 1:
            raise ValueError("User id not found.")
        return value

    @validator("title")
    def secure_title(cls, value):
        if len(value) > 32:
            ValueError("Title is too long.")
        return value
