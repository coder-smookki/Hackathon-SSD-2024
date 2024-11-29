from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.get_vcc import StateVcc
from bot.core.api.api_vks import AsyncAPIClient
from bot.core.states.get_vcc import FiltersState
from bot.core.utils.get_vcc import refactor_meetings
from bot.keyboards.get_vcc import get_filters_keyboard

filter_state_router = Router(name=__name__)


@filter_state_router.callback_query(FiltersState.base, StateVcc.filter())
async def filter_state_date(
    callback: CallbackQuery,
    callback_data: StateVcc,
    state: FSMContext,
    api_client: AsyncAPIClient,
    token: str,
):
    """Изменение поля в фильтрации "состояние" """
    await state.update_data(state=callback_data.name, page=1)
    data = await state.get_data()
    meetings, meetings_count = await api_client.get_meetings(
        token, 1, data["date_from"], data["date_to"], callback_data.name, data["filter"]
    )
    try:
        await callback.message.edit_text(
            refactor_meetings(meetings),
            reply_markup=get_filters_keyboard(meetings_count, 1),
        )
    except TelegramBadRequest:
        await callback.answer()
