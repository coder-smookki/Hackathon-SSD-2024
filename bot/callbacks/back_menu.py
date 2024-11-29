from aiogram.filters.callback_data import CallbackData


class BackMenu(CallbackData, prefix="back_menu"):
    back_menu: str
