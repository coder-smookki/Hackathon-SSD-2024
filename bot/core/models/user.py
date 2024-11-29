from datetime import date, datetime

from pydantic import Field

from bot.core.models.base import BaseCoreModel

MAX_USER_NAME_LENGTH = 128
MAX_USER_EMAIL_AND_NAME = 254


class User(BaseCoreModel):
    tg_id: int
    login: str = Field(min_length=1, max_length=MAX_USER_NAME_LENGTH)
    email: str = Field(min_length=1, max_length=MAX_USER_EMAIL_AND_NAME)

    token: str
    token_expired_at: datetime
    refresh_token: str
    refresh_token_expired_at: datetime

    vcc_id: int
    first_name: str
    last_name: str
    midle_name: str | None = Field(default=None)
    birthday: date | None = Field(default=None)
    phone: str | None = Field(default=None)
