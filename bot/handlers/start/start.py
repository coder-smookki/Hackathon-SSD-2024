from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.utils.enums import SlashCommands, TextCommands
from bot.handlers.start.formulations import START_TEXT, HELP_TEXT
from bot.keyboards.start import start_keyboard
from bot.utils.utils import extract_username
from bot.handlers.menu.main_menu import cmd_menu


router = Router(name=__name__)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, token) -> None:
    if token:
        await message.reply('⚙️ Вы уже авторизованы\n\n📍Если вы хотите выйти с аккаунта, то нажмите - [🚪] Выйти из аккаунта.')

        await cmd_menu(message=message, state=state)
    else:
        await message.answer(text=START_TEXT.format(name=extract_username(message.from_user)),
                            reply_markup=start_keyboard)
        await state.clear()


@router.message(Command(SlashCommands.HELP))
@router.message(F.text == TextCommands.HELP)
async def cmd_help(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(text=HELP_TEXT, 
                         reply_markup=start_keyboard)
