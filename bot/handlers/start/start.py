from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.core.utils.enums import SlashCommands, TextCommands
from bot.handlers.start.formulations import START_TEXT, HELP_TEXT
from bot.keyboards.start import start_keyboard


router = Router(name=__name__)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    token = data.get('token')
    if token:
        # какого хуя мы даем пользователю его токен
        await message.answer(f"Ваш токен: {token}")
    else:
        await message.answer("Токен не найден. Пройдите авторизацию.")
    # какого хуя если мы уже авторизованы у нас по новой идет авторизация
    await message.answer(text=START_TEXT,
                         reply_markup=start_keyboard)
    await state.clear()


@router.message(Command(SlashCommands.HELP))
@router.message(F.text == TextCommands.HELP)
async def cmd_help(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(text=HELP_TEXT, 
                         reply_markup=start_keyboard)
