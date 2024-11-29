from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Update
from cachetools import TTLCache

from bot.middlewares.base_information import BaseInfoMiddleware


class ThrottlingMiddleware(BaseInfoMiddleware):
    RATE_LIMIT = 2.0

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        if (user := data.get("event_from_user")) is not None:
            if user.id in self.cache:
                return None

            self.cache[user.id] = None

        return await handler(event, data)