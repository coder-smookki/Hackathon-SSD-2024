from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.create_vcc import ChooseBackendVcc
from bot.callbacks.universal import YesNo
from bot.handlers.create_vcc.state import CreateVccState, VinteoSettingsState
from bot.keyboards.create_vcc import stop_add_users
from bot.keyboards.universal import yes_no_keyboard

vinteo_vcc_router = Router(name=__name__)


@vinteo_vcc_router.callback_query(
    CreateVccState.backend, ChooseBackendVcc.filter(F.name == "vinteo")
)
async def start_get_external_settings(
    callback: CallbackQuery,
    state: FSMContext,
):
    """сохранение backend, запрос need_video_recording"""
    await state.update_data(backend="vinteo")
    await state.set_state(VinteoSettingsState.need_video_recording)
    await callback.message.edit_text(
        text="📍 Включать ли видео запись?", reply_markup=yes_no_keyboard
    )


@vinteo_vcc_router.callback_query(
    VinteoSettingsState.need_video_recording, YesNo.filter()
)
async def start_get_external_settings(
    callback: CallbackQuery,
    callback_data: YesNo,
    state: FSMContext,
):
    """сохранение need_video_recording, запрос на проверку данных"""
    await state.update_data(
        settings={"needVideoRecording": callback_data.result == "Да"}
    )
    await state.set_state(CreateVccState.participants)
    await state.update_data(participants=[])
    await callback.message.edit_text(
        "✉️ Введите email пользователей для добавления в ВКС",
        reply_markup=stop_add_users,
    )
