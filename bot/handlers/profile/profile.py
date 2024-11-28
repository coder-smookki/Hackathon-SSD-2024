from aiogram import Router, F
from aiogram.types import Message, CallbackQuery


from typing import Dict, Any
from bot.callbacks.profile import ProfileOpen
from bot.filters.role import EmailExistsFilter


router = Router(name=__name__)


@router.callback_query(ProfileOpen.filter(F.operation_prof == "profile"), EmailExistsFilter())
async def cmd_profile(callback: CallbackQuery):
    await callback.message.answer("Вы находитесь в профиле")
