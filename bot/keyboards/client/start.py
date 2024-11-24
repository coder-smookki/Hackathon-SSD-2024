from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from callbacks.client import ProfileAuthorization, ProfileOpen
from core.utils.enums import Operation

start_reply_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Авторизация",
                callback_data=ProfileAuthorization(operation_auth=Operation.AUTHORIZATIONS).pack()
            ),
        ],
        [InlineKeyboardButton(text='Профиль',
                              callback_data=ProfileOpen(operation_prof=Operation.PROFILE).pack()
                              )]
    ]
)