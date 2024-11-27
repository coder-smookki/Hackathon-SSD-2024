from pydantic import Field

from bot.core.models.base import BaseCoreModel

MAX_USER_NAME_LENGTH = 128
MAX_USER_EMAIL_AND_NAME = 254


class User(BaseCoreModel):
    tg_id: int
    login: str | None = Field(min_length=1, max_length=MAX_USER_EMAIL_AND_NAME)
    password: str = Field(min_length=1, max_length=MAX_USER_NAME_LENGTH)
    jwt_token: str
