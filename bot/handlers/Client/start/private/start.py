from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.enums import SlashCommands, TextCommands
from bot.handlers.Client.start.private.formulations import START_TEXT, HELP_TEXT
from bot.keyboards.client.start import start_reply_keyboard


router = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(text=START_TEXT,
                         reply_markup=start_reply_keyboard)


@router.message(Command(SlashCommands.HELP))
@router.message(F.text == TextCommands.HELP)
async def cmd_help(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(text=HELP_TEXT)
