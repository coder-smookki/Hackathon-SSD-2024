from aiogram.filters.callback_data import CallbackData

class Logout(CallbackData, prefix='logout'):

    operation_logout: str