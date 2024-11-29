from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.core.states.get_vcc import FiltersState
from bot.core.utils.get_vcc import refactor_meetings
from bot.core.api.api_vks import AsyncAPIClient
from bot.keyboards.get_vcc import (
    get_filters_keyboard, 
    priority_keyboard, 
)
from bot.callbacks.get_vcc import FilterVcc, PriorityVcc


filter_priority_router = Router(name=__name__)


@filter_priority_router.callback_query(
        FiltersState.base,
        FilterVcc.filter(F.name == "priority")
    )
async def filter_priority_date(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    await state.set_state(FiltersState.priority)
    await callback.message.edit_text(
        "выберите приоритет",
        reply_markup=priority_keyboard
    )

@filter_priority_router.callback_query(
        FiltersState.priority,
        PriorityVcc.filter()
    )
async def filter_priority_date(
        callback: CallbackQuery, 
        callback_data: PriorityVcc,
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    data = await state.get_data()
    data["filter"]["priority"] = callback_data.value
    await state.update_data(filter=data["filter"], page=1)
    await state.set_state(FiltersState.base)
    meetings, meetings_count = await api_client.get_meetings(
        token, 1,
        data["date_from"],
        data["date_to"],
        data["state"],
        data["filter"])
    await callback.message.edit_text(
        refactor_meetings(meetings),
        reply_markup=get_filters_keyboard(meetings_count, 1)
    )