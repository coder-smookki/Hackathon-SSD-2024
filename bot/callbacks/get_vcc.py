from aiogram.filters.callback_data import CallbackData


class StartGetVcc(CallbackData, prefix="start_get_vcc"):
    name: str

class FilterVcc(CallbackData, prefix="filter_vcc"):
    name: str

class PriorityVcc(CallbackData, prefix="priority_vcc"):
    value: int

class DepartmenVcc(CallbackData, prefix="departmen_vcc"):
    id: int

class StateVcc(CallbackData, prefix="state_vcc"):
    name: str

class PagionationVccData(CallbackData, prefix="pagination_vcc"):
    value: int # -1 or 1

class CancelFilterDataVcc(CallbackData, prefix="cancel_filter_vcc"):
    filter_: str