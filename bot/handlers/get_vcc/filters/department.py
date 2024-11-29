from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.core.states.get_vcc import FiltersState
from bot.core.utils.get_vcc import refactor_meetings
from bot.core.api.api_vks import AsyncAPIClient
from bot.keyboards.get_vcc import (
    get_filters_keyboard, 
    create_choose_department_keyboard,
)
from bot.callbacks.get_vcc import FilterVcc, DepartmenVcc


""" 
Эндпоинты с Фильтрами для запроса
"""

filter_department_router = Router(name=__name__)


@filter_department_router.callback_query(
        FiltersState.base,
        FilterVcc.filter(F.name == "department")
)
async def filter_department_datd(
        callback: CallbackQuery, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    await state.set_state(FiltersState.department)
    departments = await api_client.get_departments(token)
    await callback.message.edit_text(
        "Выберите депортамент", # TODO нету кнопки отмены 
        reply_markup=create_choose_department_keyboard(departments["data"]["data"])
    )

@filter_department_router.callback_query(
        FiltersState.department,
        DepartmenVcc.filter()
)
async def get_filter_department_data(
        callback: CallbackQuery, 
        callback_data: DepartmenVcc,
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    data = await state.get_data()
    data["filter"]["departmentId"] = callback_data.id
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