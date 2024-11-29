from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Update
from aiogram.types import User as TGUser
from aiogram import BaseMiddleware

from bot.core.models import User
from database.models import UserModel
from database.repositories import UserAlchemyRepo


class UserContextMiddleware(BaseMiddleware):
    """Мидлварь, который добавляет информацию о юзере из бд в контекст."""

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        user_repo: UserAlchemyRepo = data["user_repo"]
        event_from_user: TGUser | None = data.get("event_from_user")

        user = await user_repo.get(event_from_user.id)
        if user:
            data["user"] = user

        return await handler(event, data)