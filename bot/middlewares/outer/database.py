from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import TelegramObject
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware для управления подключением к базе данных.
    Создаёт и передаёт сессию базы данных в хэндлер.
    """

    def __init__(
        self,
        session_maker: "async_sessionmaker[AsyncSession]",
        session_key: str = "session",
    ) -> None:
        """
        Инициализация middleware.

        :param session_maker: Экземпляр async_sessionmaker для создания сессий базы данных.
        :param session_key: Ключ, под которым сессия будет передана в data (по умолчанию "db_session").
        """
        self.session_maker = session_maker
        self.session_key = session_key

    async def __call__(
        self,
        handler: "Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]",
        event: "TelegramObject",
        data: "dict[str, Any]",
    ) -> Any:
        """
        Основная логика middleware.

        :param handler: Хэндлер, который будет вызван после middleware.
        :param event: TelegramObject (например, Message или CallbackQuery).
        :param data: Словарь данных, передаваемый хэндлеру.
        """
        async with self.session_maker() as session:
            data[self.session_key] = session  # Передаём сессию в data
            return await handler(event, data)
