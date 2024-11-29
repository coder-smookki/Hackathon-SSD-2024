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


external_vcc_router = Router(name=__name__)
@external_vcc_router.callback_query(
    CreateVccState.backend, 
    ChooseBackendVcc.filter(F.name == "external")
)
async def start_get_external_settings(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    """ сохранение backend, запрос external_url """
    await state.update_data(backend = "external")
    await state.set_state(ExternalSettingsState.external_url)
    await callback.message.edit_text(
        text = "📎 Введите ссылку:",
    )

@external_vcc_router.message(ExternalSettingsState.external_url)
async def start_get_external_settings(
        message: Message, 
        state: FSMContext,
    ):
    """ сохранение external_url, запрос на проверку данных """
    await state.update_data(settings = {
        "externalUrl": message.text
    })

    await state.set_state(CreateVccState.participants)
    await state.update_data(participants=[])
    await message.answer(
        "✉️ Введите email пользователей для добавления в ВКС", 
        reply_markup=stop_add_users
    )