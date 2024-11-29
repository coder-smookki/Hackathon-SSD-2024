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


base_data_vcc_router = Router(name=__name__)


@base_data_vcc_router.callback_query(StartCreateVcc.filter())
async def start_create(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    """ Старт создания, запрос имени """
    await state.set_state(CreateVccState.name)
    await callback.message.edit_text("📋 Введите название ВКС:")


@base_data_vcc_router.message(CreateVccState.name)
async def get_name(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение имени, запрос даты проведения """
    await state.update_data(name=message.text)
    await state.set_state(CreateVccState.date)
    await message.answer("⌛ Введите дату в формате ДД ММ ГГГГ ЧЧ ММ (год месяц день час минута):\n\n⚙️ Пример: 28 11 2024 10 10")

@base_data_vcc_router.message(CreateVccState.date)
async def get_date(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение запрос даты проведения, запрос времени мероприятия """
    try:
        update_data = parse_datetime(message.text)
    except Exception:
        await message.answer("❌ Вы ввели неверную дату\n\n⚙️ Пример: 28 11 2024 10 10")
        return

    await state.update_data(date=update_data)
    await state.set_state(CreateVccState.duration)
    await message.answer("⌛ Введите продолжительность ВКС в минутах:")


@base_data_vcc_router.message(CreateVccState.duration)
async def get_duration(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение времени мероприятия, запрос максимального количества """
    try:
        data = int(message.text)
    except ValueError:
        await message.answer("❌ Вы ввели не число!")
        return
    await state.update_data(duration=data)
    await state.set_state(CreateVccState.participants_count_vks)
    await message.answer("🙍 Введите максимальное количество людей в ВКС:")


@base_data_vcc_router.message(CreateVccState.participants_count_vks)
async def get_participants_count(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение максимального количества, запрос backend """
    try:
        data = int(message.text)
    except ValueError:
        await message.answer("❌ Вы ввели не число!")
        return
    await state.update_data(participants_count=data)
    await state.set_state(CreateVccState.backend)
    await message.answer(
        "⚙️ Выберите тип ВКС:", 
        reply_markup=choose_backend_keyboard
    )