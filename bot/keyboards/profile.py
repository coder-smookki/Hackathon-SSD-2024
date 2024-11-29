from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.back_menu import BackMenu
from bot.core.utils.enums import Operation, TextCommands

profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=TextCommands.BACK_MENU,
                callback_data=BackMenu(back_menu=Operation.BACK_MENU).pack(),
            ),
        ]
    ]
)
