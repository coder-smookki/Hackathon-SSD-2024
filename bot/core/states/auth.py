from aiogram.fsm.state import StatesGroup, State


class ExtractData(StatesGroup):
    """Установление состояний: login, password, confirm"""
    email = State()
    password = State()
    confirm_check_data = State() # Согласие на достоверность данных