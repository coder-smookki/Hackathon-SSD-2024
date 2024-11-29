from aiogram.fsm.state import StatesGroup, State


class CreateVccState(StatesGroup):
    name = State()
    date = State()
    duration = State()
    participants_count_vks = State()
    participants = State()
    backend = State() # [ cisco, external, vinteo ]

    set_room = State() # будем ли мы выбирать команту
    building = State()
    room = State()

    

    check_data = State() # Проверка на корректность


class CiscoSettingsState(StatesGroup):
    is_microphone_on = State()
    is_video_on = State()
    is_waiting_room_enabled = State()
    need_video_recording = State()

class ExternalSettingsState(StatesGroup):
    external_url = State()

class VinteoSettingsState(StatesGroup):
    need_video_recording = State()