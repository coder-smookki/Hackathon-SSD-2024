from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.back_menu import BackMenu
from bot.core.utils.enums import SlashCommands
from bot.core.utils.utils import extract_username
from bot.handlers.menu.formulations import MENU_TEXT
from bot.keyboards.main_menu import main_menu_inline_keyboard

main_menu_router = Router(name=__name__)
back_menu_router = Router(name=__name__)

""" это для проверки авторизации"""


@main_menu_router.message(Command(SlashCommands.MENU))
async def cmd_menu(message: Message, state: FSMContext):
    await message.answer(
        text=MENU_TEXT.format(name=extract_username(message.from_user)),
        reply_markup=main_menu_inline_keyboard,
    )
    await state.clear()


@back_menu_router.callback_query(BackMenu.filter(F.back_menu == "back_menu"))
async def cmd_back_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        text=MENU_TEXT.format(name=extract_username(callback.message.from_user)),
        reply_markup=main_menu_inline_keyboard,
    )

    await state.clear()
