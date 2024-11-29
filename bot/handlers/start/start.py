from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.utils.enums import SlashCommands, TextCommands
from bot.core.utils.utils import extract_username
from bot.handlers.menu.main_menu import cmd_menu
from bot.handlers.start.formulations import HELP_TEXT, START_TEXT
from bot.keyboards.start import start_keyboard
from bot.keyboards.universal import back_menu_keyboard

start_router = Router(name=__name__)


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, token) -> None:
    if token:
        await message.reply(
            "⚙️ Вы уже авторизованы\n\n📍Если вы хотите выйти с аккаунта, то нажмите - [🚪] Выйти из аккаунта.",
        )

        await cmd_menu(message=message, state=state)
    else:
        await message.answer(
            text=START_TEXT.format(name=extract_username(message.from_user)),
            reply_markup=start_keyboard,
        )
        await state.clear()


@start_router.message(Command(SlashCommands.HELP))
@start_router.message(F.text == TextCommands.HELP)
async def cmd_help(message: Message, state: FSMContext, token) -> None:
    await state.clear()
    if token:
        await message.answer(text=HELP_TEXT, reply_markup=back_menu_keyboard)
    else:
        await message.answer(text=HELP_TEXT, reply_markup=start_keyboard)
