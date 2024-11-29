from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from bot.callbacks.create_vcc import StartCreateVcc
from bot.callbacks.get_vcc import StartGetVcc
from bot.callbacks.logout import Logout
from bot.callbacks.profile import ProfileOpen
from bot.core.utils.enums import Operation, TextCommands

main_menu_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=TextCommands.VIEW_VKS, callback_data=StartGetVcc().pack()
            ),
            InlineKeyboardButton(
                text=TextCommands.CREATE_VKS, callback_data=StartCreateVcc().pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text=TextCommands.PROFILE,
                callback_data=ProfileOpen(operation_prof=Operation.PROFILE).pack(),
            )
        ],
        [InlineKeyboardButton(text=TextCommands.LOGOUT, callback_data=Logout().pack())],
    ]
)

main_menu_keyoard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Главное меню")]]
)
