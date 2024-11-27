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


main_menu_router = Router(name=__name__)


@main_menu_router.message(Command(SlashCommands.MENU))
#@main_menu_router.message(F.text == TextCommands.MAIN_MENU)
async def cmd_menu(message: Message, state: FSMContext) -> None:
    await message.answer(text=MAIN_MENU_TEXT.format(name=extract_username(message.from_user)),
                        reply_markup=main_menu_inline_keyboard)
    await state.clear()

# from aiogram import Router, F
# from aiogram.types import Message


# main_menu_router = Router(name=__name__)

# """ это для проверки авторизации"""
# @main_menu_router.message(F.text == "Главное меню")
# async def cmd_profile(message: Message, token):
#     print(token)
#     await message.answer("Вы находитесь в профиле")
