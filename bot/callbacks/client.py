from aiogram.filters.callback_data import CallbackData


class ProfileAuthorization(CallbackData, prefix='authorization'):
    '''Фабрика для авторизации пользователся'''

    operation_auth: str


class ProfileOpen(CallbackData, prefix='profile'):
    '''Фабрика для открытие профиля'''

    operation_prof: str
