from aiogram import Router, F
from aiogram.types import Message


main_menu_router = Router(name=__name__)

""" это для проверки авторизации"""
@main_menu_router.message(F.text == "Главное меню")
async def cmd_profile(message: Message, token):
    print(token)
    await message.answer("Вы находитесь в профиле")
