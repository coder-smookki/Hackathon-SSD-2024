from aiogram.filters.callback_data import CallbackData


class StartCreateVcc(CallbackData, prefix="start_create_vcc"):
    ...


class ChooseBackendVcc(CallbackData, prefix="choose_backend_for_create_vcc"):
    name: str


class ChooseBuilding(CallbackData, prefix="choose_building_for_create_vcc"):
    id: int

class ChooseRoom(CallbackData, prefix="choose_room_for_create_vcc"):
    id: int