from collections.abc import Callable
from typing import Any

from aiogram import BaseMiddleware, Bot, Router
from aiogram.types import Chat, TelegramObject


class AuthMiddleware(BaseMiddleware):
    """
    Middleware для авторизации, выполняется только при состоянии confirm.
    """

    def __init__(self, exceptions_router: list[str]):
        self.exceptions_router = exceptions_router
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Any],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """
        Выполнение middleware при достижении состояния ExtractData.confirm.
        """
        # TODO
        bot: Bot = data["bot"]
        event_chat: Chat | None = data.get("event_chat")
        event_router: Router | None = data.get("event_router")

        if event_router is not None and event_router.name in self.exceptions_router:
            return await handler(event, data)

        if data.get("token") is not None:
            return await handler(event, data)

        await bot.send_message(event_chat.id, "Неизвестный юзер.\nНажмите /start")
