from aiogram.filters.callback_data import CallbackData


class YesNo(CallbackData, prefix="yes_no"):
    result: str