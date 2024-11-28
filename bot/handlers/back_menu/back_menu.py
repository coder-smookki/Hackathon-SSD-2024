from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Dict, Any

from bot.core.utils.enums import SlashCommands, TextCommands
from bot.handlers.start.formulations import MAIN_MENU_TEXT
from bot.keyboards.main_menu import main_menu_inline_keyboard
from bot.handlers.profile.profile import cmd_profile
from bot.utils.utils import extract_username
from bot.callbacks.back_menu import BackMenu


back_menu_router = Router(name=__name__)


@back_menu_router.callback_query(BackMenu.filter(F.back_menu == "back_menu"))
async def cmd_back_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(text=MAIN_MENU_TEXT.format(name=extract_username(callback.message.from_user)))
    
    await callback.message.edit_reply_markup(reply_markup=main_menu_inline_keyboard)
    await state.clear()
