from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiohttp import ClientSession

from bot.core.api.api_vks import AsyncAPIClient
from database.repositories import UserAlchemyRepo


class ServiceDIMiddleware(BaseMiddleware):
    """Мидлварь для добавления сервисов в контекст обработчиков телеграма."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        session = data["session"]

        user_repo = UserAlchemyRepo(session)

        api_client = AsyncAPIClient()
        print(api_client, "API CLIENT"*5)

        data.update(
            user_repo=user_repo,
            api_client=api_client
        )

        return await handler(event, data)