from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.get_vcc import CancelFilterDataVcc
from bot.core.api.api_vks import AsyncAPIClient
from bot.core.states.get_vcc import FiltersState
from bot.core.utils.get_vcc import refactor_meetings
from bot.keyboards.get_vcc import get_filters_keyboard

filter_cancel_router = Router(name=__name__)


@filter_cancel_router.callback_query(CancelFilterDataVcc.filter())
async def cancel_filter(
    callback: CallbackQuery,
    callback_data: CancelFilterDataVcc,
    state: FSMContext,
    api_client: AsyncAPIClient,
    token: str,
):
    data = await state.get_data()
    data["filter"].pop(callback_data.filter_, None)
    await state.update_data(filter=data["filter"], page=1)
    await state.set_state(FiltersState.base)
    meetings, meetings_count = await api_client.get_meetings(
        token,
        1,
        data["date_from"],
        data["date_to"],
        data["state"],
        data["filter"],
    )
    await callback.message.edit_text(
        refactor_meetings(meetings),
        reply_markup=get_filters_keyboard(meetings_count, 1),
    )
