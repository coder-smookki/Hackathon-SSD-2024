from aiogram.fsm.state import StatesGroup, State


class GetVccState(StatesGroup):
    date_from = State()
    date_to = State()


class FiltersState(StatesGroup):
    base = State()
    priority = State()
    department = State()
    name = State()
    user = State()