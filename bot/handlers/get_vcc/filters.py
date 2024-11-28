from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.handlers.get_vcc.state import FiltersState
from bot.handlers.get_vcc.utils import refactor_meeting, refactor_meetings
from bot.core.utils.utils import is_valid_email
from bot.core.api.api_vks import AsyncAPIClient
from bot.keyboards.get_vcc import (
    get_filters_keyboard, 
    priority_keyboard, 
    create_choose_department_keyboard,
    cancel_name_keyboard,
    cancel_user_keyboard
)
from bot.callbacks.get_vcc import (
    StateVcc, 
    FilterVcc, 
    PriorityVcc, 
    DepartmenVcc, 
    CancelFilterDataVcc
)
from bot.callbacks.state import InStateData


""" 
Эндпоинты с Фильтрами для запроса
"""

filter_router = Router(name=__name__)


@filter_router.callback_query(
        FiltersState.base,
        StateVcc.filter()
    )
async def filter_state_date(
        callback: CallbackQuery, 
        callback_data: StateVcc,
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    """ Изменение поля в фильтрации "состояние" """
    await state.update_data(state=callback_data.name, page=1)
    data = await state.get_data()
    meetings, meetings_count = await api_client.get_meetings(
        token, 1, 
        data["date_from"], 
        data["date_to"], 
        callback_data.name,
        data["filter"]
    )
    #result = [refactor_meeting(meeting) for meeting in meetings]
    await callback.message.edit_text(
        #str(result), 
        refactor_meetings(meetings), 
        reply_markup=get_filters_keyboard(meetings_count, 1))



@filter_router.callback_query(
        FiltersState.base,
        FilterVcc.filter(F.name == "name")
    )
async def filter_state_date(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    await state.set_state(FiltersState.name)
    await callback.message.answer("Введите текст для поиска", reply_markup=cancel_name_keyboard)
    await callback.answer()

@filter_router.message(FiltersState.name)
async def get_filter_state_date(
        message: Message, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    data = await state.get_data()
    data["filter"]["filter"] = message.text
    await state.update_data(filter=data["filter"], page=1)
    await state.set_state(FiltersState.base)
    meetings, meetings_count = await api_client.get_meetings(
        token, 1,
        data["date_from"],
        data["date_to"],
        data["state"],
        data["filter"])
    await message.answer(
        #str([refactor_meeting(meeting) for meeting in meetings]), 
        refactor_meetings(meetings),
        reply_markup=get_filters_keyboard(meetings_count, 1)
    )



@filter_router.callback_query(
        FiltersState.base,
        FilterVcc.filter(F.name == "priority")
    )
async def filter_priority_date(
        callback: CallbackQuery, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    await state.set_state(FiltersState.priority)
    await callback.message.edit_text(
        "выберите приоритет",
        reply_markup=priority_keyboard
    )

@filter_router.callback_query(
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
        #str([refactor_meeting(meeting) for meeting in meetings]), 
        refactor_meetings(meetings),
        reply_markup=get_filters_keyboard(meetings_count, 1)
    )



@filter_router.callback_query(
        FiltersState.base,
        FilterVcc.filter(F.name == "user")
)
async def filter_user_date(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    await state.set_state(FiltersState.user)
    await callback.message.edit_text("Введите Имейл админа", reply_markup=cancel_user_keyboard)

@filter_router.message(FiltersState.user)
async def get_filter_user_date(
        message: Message,
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    if not is_valid_email(message.text):
        await message.answer("это не имейл", reply_markup=cancel_user_keyboard)
        return
    user_data = await api_client.get_user(token, message.text)
    if not user_data["data"]["data"]:
        await message.answer("этого юзера нету в бд", reply_markup=cancel_user_keyboard)
        return
    data = await state.get_data()
    data["filter"]["userId"] = user_data["data"]["data"][0]["id"]
    await state.update_data(filter=data["filter"], page=1)
    await state.set_state(FiltersState.base)
    meetings, meetings_count = await api_client.get_meetings(
        token, 1,
        data["date_from"],
        data["date_to"],
        data["state"],
        data["filter"])
    await message.answer(
        #str([refactor_meeting(meeting) for meeting in meetings]), 
        refactor_meetings(meetings),
        reply_markup=get_filters_keyboard(meetings_count, 1)
    )



@filter_router.callback_query(
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

@filter_router.callback_query(
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



@filter_router.callback_query(
        CancelFilterDataVcc.filter()
)
async def cancel_filter(
        callback: CallbackQuery, 
        callback_data: CancelFilterDataVcc,
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    data = await state.get_data()
    data["filter"].pop(callback_data.filter_, None)
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

