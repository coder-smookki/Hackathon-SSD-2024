from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Dict, Any

from bot.core.utils.enums import SlashCommands, TextCommands
from bot.handlers.start.formulations import START_TEXT, HELP_TEXT
from bot.keyboards.start import start_keyboard
from bot.handlers.profile.profile import cmd_profile
from bot.handlers.main_menu.main_menu import cmd_menu
from bot.utils.utils import extract_username


router = Router(name=__name__)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, token) -> None:
    if token:
        # callback = CallbackQuery(
        #     id="start_profile_redirect",
        #     from_user=message.from_user,
        #     message=message,
        #     chat_instance="-",
        #     data="profile"
        # )
        # await cmd_profile(callback=callback)

        await message.reply('Вы уже авторизованы')

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
