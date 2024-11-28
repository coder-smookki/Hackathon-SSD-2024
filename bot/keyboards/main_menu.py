from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.state import InStateData
from bot.core.utils.enums import Operation
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.callbacks.profile import ProfileOpen
from bot.callbacks.logout import Logout
from bot.callbacks.view_vks import ViewVKS
from bot.callbacks.authorization import Authorization
from bot.core.utils.enums import Operation
from bot.core.utils.enums import TextCommands
from bot.callbacks.create_vcc import StartCreateVcc




main_menu_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=TextCommands.VIEW_VKS,
                callback_data=ViewVKS(operation_view_vks=Operation.VIEW_VKS).pack()
            ),
            InlineKeyboardButton(
                text=TextCommands.CREATE_VKS,
                callback_data=StartCreateVcc().pack()
            )
        ],
        [
            InlineKeyboardButton(
                text=TextCommands.PROFILE,
                callback_data=ProfileOpen(operation_prof=Operation.PROFILE).pack()
            )
        ],
        # [
        #     InlineKeyboardButton(
        #         text=TextCommands.LOGOUT,
        #         callback_data=Logout(operation_logout=Operation.LOGOUT).pack()
        #     )
        # ]
    ]
)

main_menu_keyoard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Главное меню")]
    ]
)