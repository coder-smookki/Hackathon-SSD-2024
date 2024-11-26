from typing import Any

from database.models.base import AlchemyBaseModel
from sqlalchemy import BigInteger, ForeignKey, Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

#
# from typing import TYPE_CHECKING
#
# from core.models.user import (
#     MAX_TG_NAME_LENGTH,
#     MAX_USER_DESCRIPTION_LENGTH,
#     MAX_USER_NAME_LENGTH,
# )
#
# if TYPE_CHECKING:
#     from database.models.city import CityModel
#     from database.models.country import CountryModel

MAX_LOGIN_LENGTH = 128
MAX_EMAIL_LENGTH = 254
MAX_PASSWORD_LENGTH = 64


class UserModel(AlchemyBaseModel):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    # login: Mapped[str] = mapped_column(String(MAX_LOGIN_LENGTH), nullable=False)
    email: Mapped[str] = mapped_column(String(MAX_EMAIL_LENGTH), nullable=False)
    password: Mapped[str] = mapped_column(String(MAX_PASSWORD_LENGTH), nullable=False)
    jwt_token: Mapped[str] = mapped_column(String(), nullable=False)
    events: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)  # С id встреч, в которых учавствует человек


    # def __init__(self, tg_id, login, email, password, jwt_token, **kw: Any):
    #     super().__init__(**kw)
    #     self.tg_id = tg_id
    #     self.login = login
    #     self.email = email
    #     self.password = password
    #     self.jwt_token = jwt_token

