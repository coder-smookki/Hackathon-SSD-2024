from aiogram import BaseMiddleware
from typing import TYPE_CHECKING, Any, Final
from aiogram.types import Message


from aiogram.fsm.context import FSMContext
from aiogram.types import User

import logging
# from shared.services.user_service import UserService
from typing import TYPE_CHECKING, cast, Union
from aiogram.types import TelegramObject, Message, User

from core.services.user import UserService


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)


class SaveUsersIdMiddleware(BaseMiddleware):
    """Middleware для сохранения данных пользователя"""
    USER_INFO_KEY: Final[str] = "user_info"

    async def __call__(
        self,
        handler: "Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]",
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        state: FSMContext = data.get("state")
        if state:
            user_data = await state.get_data()
            if user_data:
                user_info = {
                    "email": user_data.get("email") or "Не указано",
                    "login": user_data.get("login") or "Не указано",
                    "password": user_data.get("password") or "Не указано",
                }
                data[self.USER_INFO_KEY] = user_info
                print(f"Данные пользователя сохранены в middleware: {user_info}")
        return await handler(event, data)

