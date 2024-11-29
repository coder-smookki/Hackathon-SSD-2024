from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.callbacks.create_vcc import (
    StartCreateVcc, 
    ChooseBackendVcc,
    ChooseBuilding,
    ChooseRoom,
    StopAddUser
)
from bot.callbacks.universal import YesNo
from bot.callbacks.state import InStateData
from bot.handlers.create_vcc.state import (
    CreateVccState,
    CiscoSettingsState,
    VinteoSettingsState,
    ExternalSettingsState
)
from bot.keyboards.create_vcc import (
    choose_backend_keyboard, 
    stop_add_users,
    create_choose_building_keyboard,
    create_choose_room_keyboard
)
from bot.keyboards.universal import yes_no_keyboard, back_menu_keyboard
from bot.core.utils.enums import Operation
from bot.core.utils.utils import parse_datetime
from bot.core.api.api_vks import AsyncAPIClient
from bot.core.utils.utils import is_valid_email
from database.models import UserModel
from bot.handlers.create_vcc.formulations import (
    CREATION_VKS_CISCO, 
    CREATION_VKS_EXTERNAL,
    CREATION_VKS_VINTEO,
    END_CREATION_VKS
)


vinteo_vcc_router = Router(name=__name__)

@vinteo_vcc_router.callback_query(
    CreateVccState.backend, 
    ChooseBackendVcc.filter(F.name == "vinteo")
)
async def start_get_external_settings(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    """ сохранение backend, запрос need_video_recording """
    await state.update_data(backend = "vinteo")
    await state.set_state(VinteoSettingsState.need_video_recording)
    await callback.message.edit_text(
        text = "📍 Включать ли видео запись?",
        reply_markup=yes_no_keyboard
    )

@vinteo_vcc_router.callback_query(
    VinteoSettingsState.need_video_recording,
    YesNo.filter()
)
async def start_get_external_settings(
        callback: CallbackQuery, 
        callback_data: YesNo,
        state: FSMContext,
    ):
    """ сохранение need_video_recording, запрос на проверку данных """
    await state.update_data(settings = {
        "needVideoRecording": callback_data.result=="Да"
    })
    await state.set_state(CreateVccState.participants)
    await state.update_data(participants=[])
    await callback.message.edit_text(
        "✉️ Введите email пользователей для добавления в ВКС", 
        reply_markup=stop_add_users
    )