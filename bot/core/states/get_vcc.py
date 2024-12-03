from aiogram.fsm.state import State, StatesGroup


class GetVccState(StatesGroup):
    date_from = State()
    date_to = State()


class FiltersState(StatesGroup):
    base = State()
    priority = State()
    department = State()
    name = State()
    user = State()
