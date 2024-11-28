from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.create_vcc import StartCreateVcc


main_menu_router = Router(name=__name__)

""" это для проверки авторизации"""
@main_menu_router.message(F.text == "Главное меню")
async def cmd_profile(message: Message, token):
    await message.answer(
        "Вы находитесь в профиле",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="создать вкс", callback_data=StartCreateVcc().pack())]
            ]
        )
    )
