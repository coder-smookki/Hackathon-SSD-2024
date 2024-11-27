from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram.types import Message
from typing import Dict, Any
from bot.callbacks.logout import Logout
from bot.filters.role import EmailExistsFilter

from sqlalchemy import select

from database.models import UserModel
from database.session import database_init
from database.settings import get_settings



logout_router = Router(name=__name__)


@logout_router.callback_query(Logout.filter(F.operation_logout == "logout"))
async def cmd_profile(callback: CallbackQuery):

    settings = get_settings()
    session_maker = await database_init(settings.db)

    async with session_maker() as session:
        await session.commit()

        result = await session.execute(select(UserModel).filter(UserModel.tg_id == callback.from_user.id))

        user = result.scalar_one_or_none()

        if user:
            user.token = None
            #user.refresh_token = None

            await session.commit()

            await callback.message.answer("Вы успешно вышли из системы.")
        else:
            await callback.message.answer("Пользователь не найден в системе.")

    await session.close()


