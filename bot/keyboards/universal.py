from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.state import InStateData
from bot.callbacks.universal import YesNo
from bot.core.utils.enums import Operation



CANCEL = f"❌ Отмена"
CONFIRM = f"✅ Подтвердить"

YES = f"Да"
NO = f"Нет"

confirm_state_button = InlineKeyboardButton(
    text=CONFIRM,
    callback_data=InStateData(action=Operation.CONFIRM).pack(),
)
cancel_state_button = InlineKeyboardButton(
    text=CANCEL,
    callback_data=InStateData(action=Operation.CANCEL).pack(),
)

cancel_state_keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_state_button]])
confirm_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[confirm_state_button, cancel_state_button]],
)


yes_no_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text=YES, callback_data=YesNo(result=YES).pack()),
        InlineKeyboardButton(text=NO, callback_data=YesNo(result=NO).pack())
    ]]
)