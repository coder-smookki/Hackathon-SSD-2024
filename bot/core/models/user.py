from pydantic import Field

from core.models.base import BaseCoreModel

MAX_USER_NAME_LENGTH = 128
MAX_USER_EMAIL = 254
MAX_TG_NAME_LENGTH = 32


class User(BaseCoreModel):
    id: int
    email: str | None = Field(None, max_length=MAX_USER_EMAIL)
    login: str | None = Field(min_length=1, max_length=MAX_TG_NAME_LENGTH)
    password: str = Field(min_length=1, max_length=MAX_USER_NAME_LENGTH)
