from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.state import InStateData
from bot.core.utils.enums import Operation


main_menu_keyoard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Главное меню")]
    ]
)