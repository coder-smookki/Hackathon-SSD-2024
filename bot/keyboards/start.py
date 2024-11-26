from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.callbacks.authorization import Authorization
from bot.core.utils.enums import Operation
from bot.core.utils.enums import TextCommands

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=TextCommands.AUTHORIZATIONS,
                callback_data=Authorization(operation_auth=Operation.AUTHORIZATIONS).pack()
            )
        ]
    ]
)