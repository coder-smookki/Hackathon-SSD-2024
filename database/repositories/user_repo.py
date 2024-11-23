from typing import cast

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserModel
from database.schemas.users import UserDTO


class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_tg_id(self, tg_id: int) -> UserDTO | None:
        query = sa.select(UserModel).where(UserModel.tg_id == tg_id)
        scalar: UserModel | None = await self._session.scalar(query)
        return UserDTO.model_validate(scalar) if scalar is not None else None

    async def save_new_user(self, tg_id: int) -> None:
        user = UserModel(tg_id=tg_id)
        self._session.add(user)
        await self._session.flush()

    async def update_user(self, tg_id: int, **kwargs) -> None:
        query = sa.update(UserModel).where(UserModel.tg_id == tg_id).values(**kwargs)
        await self._session.execute(query)
        await self._session.flush()

    async def get_user_by_email(self, email: str) -> UserDTO | None:
        query = sa.select(UserModel).where(UserModel.email == email)
        scalar: UserModel | None = await self._session.scalar(query)
        return UserDTO.model_validate(scalar) if scalar is not None else None
