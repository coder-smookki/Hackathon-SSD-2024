from aiogram.filters.callback_data import CallbackData


class Authorization(CallbackData, prefix="authorization"):
    """Фабрика для авторизации пользователся и входа профиля"""

    operation_auth: str
