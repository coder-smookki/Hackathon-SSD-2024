from aiogram import BaseMiddleware
from typing import TYPE_CHECKING, Any, Final
from aiogram.types import Message


from aiogram.fsm.context import FSMContext
from aiogram.types import User

import logging
# from shared.services.user_service import UserService
from typing import TYPE_CHECKING, cast, Union


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from aiogram.types import TelegramObject, Message, User

logger = logging.getLogger(__name__)


class SaveUsersIdMiddleware(BaseMiddleware):
    USER_INFO_KEY: Final[str] = "user_info"

    async def __call__(
            self,
            handler: "Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]",
            event: "TelegramObject",
            data: dict[str, Any],
    ) -> Any:
        if user := data.get("event_from_user"):
            # user_id = user.id
            user_info = {
                "id": user.id,
                "email": data.get("email"),
                "login": data.get("login"),
                "password": data.get("password")
            }
            # data[self.USER_ID_KEY] = user.id
            # print(f"Сохраненный ID пользователя: {user_id}")
            data[self.USER_INFO_KEY] = user_info

            # Выводим информацию о пользователе
            print(f"Сохраненные данные пользователя: {user_info}")
        else:
            data[self.USER_INFO_KEY] = None

        return await handler(event, data)
