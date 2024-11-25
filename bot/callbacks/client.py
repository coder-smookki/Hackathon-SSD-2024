from aiogram.filters.callback_data import CallbackData


class ProfileAuthorization(CallbackData, prefix='authorization'):
    '''Фабрика для авторизации пользователся и входа профиля'''

    operation_auth: str
    # open_profile: bool
    

class ProfileOpen(CallbackData, prefix='profile'):
    '''Фабрика для открытие профиля'''

    operation_prof: str
