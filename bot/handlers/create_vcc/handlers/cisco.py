from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.create_vcc import ChooseBackendVcc
from bot.callbacks.universal import YesNo
from bot.handlers.create_vcc.state import CiscoSettingsState, CreateVccState
from bot.keyboards.create_vcc import stop_add_users
from bot.keyboards.universal import yes_no_keyboard

cisco_vcc_router = Router(name=__name__)


@cisco_vcc_router.callback_query(
    CreateVccState.backend, ChooseBackendVcc.filter(F.name == "cisco")
)
async def start_get_cisco_settings(
    callback: CallbackQuery,
    state: FSMContext,
):
    """сохранение backend, запрос is_microphone_on"""
    await state.update_data(backend="cisco")
    await state.set_state(CiscoSettingsState.is_microphone_on)
    await callback.message.edit_text(
        text="📍 Включать ли микрофон обязательно?", reply_markup=yes_no_keyboard
    )


@cisco_vcc_router.callback_query(CiscoSettingsState.is_microphone_on, YesNo.filter())
async def start_get_cisco_settings(
    callback: CallbackQuery,
    callback_data: YesNo,
    state: FSMContext,
):
    """сохранение is_microphone_on, запрос is_video_on"""
    await state.update_data(is_microphone_on=callback_data.result == "Да")
    await state.set_state(CiscoSettingsState.is_video_on)
    await callback.message.edit_text(
        text="📍 Включать ли видео обязательно?", reply_markup=yes_no_keyboard
    )


@cisco_vcc_router.callback_query(CiscoSettingsState.is_video_on, YesNo.filter())
async def start_get_cisco_settings(
    callback: CallbackQuery,
    callback_data: YesNo,
    state: FSMContext,
):
    """сохранение is_video_on, запрос is_waiting_room_enabled"""
    await state.update_data(is_video_on=callback_data.result == "Да")
    await state.set_state(CiscoSettingsState.is_waiting_room_enabled)
    await callback.message.edit_text(
        text="📍 Включать ли ожидание ВКС?", reply_markup=yes_no_keyboard
    )


@cisco_vcc_router.callback_query(
    CiscoSettingsState.is_waiting_room_enabled, YesNo.filter()
)
async def start_get_cisco_settings(
    callback: CallbackQuery,
    callback_data: YesNo,
    state: FSMContext,
):
    """сохранение is_waiting_room_enabled, запрос need_video_recording"""
    await state.update_data(is_waiting_room_enabled=callback_data.result == "Да")
    await state.set_state(CiscoSettingsState.need_video_recording)
    await callback.message.edit_text(
        text="📍 Включать ли видео запись?", reply_markup=yes_no_keyboard
    )


@cisco_vcc_router.callback_query(
    CiscoSettingsState.need_video_recording, YesNo.filter()
)
async def start_get_cisco_settings(
    callback: CallbackQuery,
    callback_data: YesNo,
    state: FSMContext,
):
    """сохранение need_video_recording, запрос на проверку данных"""
    data = await state.get_data()
    await state.update_data(
        settings={
            "isMicrophoneOn": data["is_microphone_on"],
            "isVideoOn": data["is_video_on"],
            "isWaitingRoomEnabled": data["is_waiting_room_enabled"],
            "needVideoRecording": callback_data.result == "Да",
        }
    )

    await state.set_state(CreateVccState.participants)
    await state.update_data(participants=[])
    await callback.message.edit_text(
        "✉️ Введите email пользователей для добавления в ВКС",
        reply_markup=stop_add_users,
    )
