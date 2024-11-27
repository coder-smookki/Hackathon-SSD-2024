from typing import Any
from datetime import date, datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, ARRAY, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import AlchemyBaseModel


MAX_LOGIN_LENGTH = 128
MAX_EMAIL_LENGTH = 254
MAX_PASSWORD_LENGTH = 64
MAX_NAME_LENGTH = 64
MAX_PHONE_LENGTH = 32


class UserModel(AlchemyBaseModel):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    login: Mapped[str] = mapped_column(String(MAX_LOGIN_LENGTH), nullable=False)
    email: Mapped[str] = mapped_column(String(MAX_EMAIL_LENGTH), nullable=False)

    token: Mapped[str] = mapped_column(String(4000), nullable=False)
    token_expired_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(1000), nullable=False)
    refresh_token_expired_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    events: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)  
    # С id встреч, в которых учавствует человек

    vcc_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    first_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    last_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)
    midle_name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=True)
    birthday: Mapped[date] = mapped_column(Date(), nullable=True)
    phone: Mapped[str] = mapped_column(String(MAX_PHONE_LENGTH), nullable=True)

    # def __init__(self, tg_id, login, email, password, jwt_token, **kw: Any):
    #     super().__init__(**kw)
    #     self.tg_id = tg_id
    #     self.login = login
    #     self.email = email
    #     self.password = password
    #     self.jwt_token = jwt_token

