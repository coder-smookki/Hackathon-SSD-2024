from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram.types import Message
from typing import Dict, Any
from aiogram.fsm.context import FSMContext
from bot.callbacks.logout import Logout
from bot.filters.role import EmailExistsFilter

from sqlalchemy import select
from core.api.api_vks import initialize_api_client

from database.models import UserModel
from database.session import database_init
from database.settings import get_settings



logout_router = Router(name=__name__)

# Почему-то не работает, и пользователя все также может пользоваться как и авторизованный
@logout_router.callback_query(Logout.filter(F.operation_logout == "logout"))
async def cmd_logout(callback: CallbackQuery, state: FSMContext):

    settings = get_settings()
    session_maker = await database_init(settings.db)

    async with session_maker() as session:
        await session.commit()

        result = await session.execute(select(UserModel).filter(UserModel.tg_id == callback.from_user.id))

        user = result.scalar_one_or_none()

        client = await initialize_api_client()
        
        response = await client.auth_logout(token=user.token)
        print(f'Logout response: {response}')

        if  response['Status'] == 'ok':
            await session.commit()
            await session.close()
            await state.clear()

            await callback.message.edit_text("Вы успешно вышли из системы.")
        else:
            await callback.message.edit_text("Пользователь не найден в системе.")




