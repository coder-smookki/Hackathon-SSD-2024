from aiogram.fsm.state import State, StatesGroup


class ExtractData(StatesGroup):
    """Установление состояний: login, password, confirm"""

    email = State()
    password = State()
    confirm_check_data = State()  # Согласие на достоверность данных
