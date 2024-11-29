from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.create_vcc import ChooseBackendVcc
from bot.handlers.create_vcc.state import CreateVccState, ExternalSettingsState
from bot.keyboards.create_vcc import stop_add_users

external_vcc_router = Router(name=__name__)


@external_vcc_router.callback_query(
    CreateVccState.backend, ChooseBackendVcc.filter(F.name == "external")
)
async def start_get_external_settings(
    callback: CallbackQuery,
    state: FSMContext,
):
    """сохранение backend, запрос external_url"""
    await state.update_data(backend="external")
    await state.set_state(ExternalSettingsState.external_url)
    await callback.message.edit_text(
        text="📎 Введите ссылку:",
    )


@external_vcc_router.message(ExternalSettingsState.external_url)
async def start_get_external_settings(
    message: Message,
    state: FSMContext,
):
    """сохранение external_url, запрос на проверку данных"""
    await state.update_data(settings={"externalUrl": message.text})

    await state.set_state(CreateVccState.participants)
    await state.update_data(participants=[])
    await message.answer(
        "✉️ Введите email пользователей для добавления в ВКС",
        reply_markup=stop_add_users,
    )
