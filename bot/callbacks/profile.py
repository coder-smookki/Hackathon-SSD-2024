from aiogram.filters.callback_data import CallbackData


class ProfileOpen(CallbackData, prefix='profile'):
    '''Фабрика для открытие профиля'''

    operation_prof: str
