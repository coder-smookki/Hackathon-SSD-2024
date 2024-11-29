from abc import ABC
from typing import Union, cast

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, User

from bot.core.utils.utils import extract_username


class BaseInfoMiddleware(BaseMiddleware, ABC):
    """Базовый мидлварь. Он нужен, чтобы метод get_short_info был везде."""

    def get_short_info(
        self,
        event: "Union[CallbackQuery, Message]",
    ) -> str | None:
        """Короткая информация о пользователе для логов."""
        from_user = cast(User, event.from_user)
        return (
            f"[id={from_user.id}, "
            f"chat_id={self.extract_chat_id(event)}, "
            f"username={extract_username(from_user)}]"
        )

    @staticmethod
    def extract_chat_id(event: "Union[CallbackQuery, Message]") -> int | None:
        """
        Получение имени для бд из сообщения или нажатия кнопки.

        :param event: Событие.
        :return: Имя пользователя.
        """
        if isinstance(event, CallbackQuery):
            event = event.message
        return event.chat.id