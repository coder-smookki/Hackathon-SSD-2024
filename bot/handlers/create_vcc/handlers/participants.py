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


participants_vcc_router = Router(name=__name__)


@participants_vcc_router.message(CreateVccState.participants)
async def get_participants(
        message: Message, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    if not is_valid_email(message.text):
        await message.answer("❌ Это не email!", reply_markup=stop_add_users)
        return
    user_data = await api_client.get_user(token, message.text)
    if not user_data["data"]["data"]:
        await message.answer("❌ Этого пользователя нету", reply_markup=stop_add_users)
        return
    data = await state.get_data()
    if {"id": user_data["data"]["data"][0]["id"]} in data["participants"]:
        await message.answer("❌ Этот пользователь уже добавлен", reply_markup=stop_add_users)
        return
    data["participants"].append({"id": user_data["data"]["data"][0]["id"]})
    await message.answer("✅ Добавлен", reply_markup=stop_add_users)


@participants_vcc_router.callback_query(
        CreateVccState.participants, 
        StopAddUser.filter()
)
async def cancel_participants(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    await state.set_state(CreateVccState.set_room)
    await callback.message.edit_text(
        text = "🔒 Хотите ли вы указать помещение ВКС?",
        reply_markup=yes_no_keyboard
    )