from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from aiogram.types import Message
from typing import Dict, Any
from bot.callbacks.profile import ProfileOpen
from bot.filters.role import EmailExistsFilter
from bot.handlers.profile.formulations import PROFILE_TEXT
from bot.core.utils.enums import SlashCommands, TextCommands
from aiogram.filters import CommandStart, Command

from sqlalchemy import select
from bot.core.api.api_vks import AsyncAPIClient

from database.models import UserModel
from database.session import database_init
from database.settings import get_settings
from bot.keyboards.profile import profile_keyboard


router = Router(name=__name__)


@router.callback_query(ProfileOpen.filter(F.operation_prof == "profile"), EmailExistsFilter())
async def cmd_profile(callback: CallbackQuery):
    
    settings = get_settings()
    session_maker = await database_init(settings.db)

    async with session_maker() as session:
        await session.commit()

        result = await session.execute(select(UserModel).filter(UserModel.tg_id == callback.from_user.id))

        user = result.scalar_one_or_none()

        await session.commit()
        await session.close()


        await callback.message.edit_text(text=PROFILE_TEXT.format(first_name=user.first_name,
                                                                  last_name=user.last_name,
                                                                  midle_name=user.midle_name,
                                                                  login=user.login,
                                                                  email=user.email,
                                                                  ), reply_markup=profile_keyboard)


    #await callback.message.edit_text("Профиль")
    #await callback.message.edit_reply_markup(reply_markup=start_keyboard)