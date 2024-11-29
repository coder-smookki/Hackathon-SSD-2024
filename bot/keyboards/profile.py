from bot.core.utils.enums import Operation
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.callbacks.authorization import Authorization
from bot.core.utils.enums import Operation
from bot.core.utils.enums import TextCommands
from bot.callbacks.back_menu import BackMenu


profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=TextCommands.BACK_MENU,
                callback_data=BackMenu(back_menu=Operation.BACK_MENU).pack()
            ),
        ]
    ]
)