from typing import Callable

from bot.core.models.user import User
from bot.core.models.user import (
    MAX_USER_NAME_LENGTH,
    MAX_USER_EMAIL,
    MAX_TG_NAME_LENGTH,
) 
from bot.core.repositories.user import UserRepo
from bot.core.utils.enums import ProfileField


class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    async def get(self, tg_id: int):
        return await self.user_repo.get(tg_id)

    async def create(self, instance: User):
        return await self.user_repo.create(instance)

    async def update(self, tg_id: int, instance: User):
        return await self.user_repo.update(tg_id, instance)