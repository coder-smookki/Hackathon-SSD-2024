from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.callbacks.get_vcc import PagionationVccData
from bot.handlers.get_vcc.formulations import SHOWING_VKS
from bot.core.api.api_vks import MEETINGS_ON_PAGE, AsyncAPIClient
from bot.handlers.get_vcc.state import FiltersState
from bot.utils.get_vcc.utils import refactor_meetings, refactor_meeting
from bot.keyboards.get_vcc import (
    get_filters_keyboard, 
    priority_keyboard, 
    create_choose_department_keyboard
)

""" 
Обработка пагинации
"""


pagination_router = Router(name=__name__)


@pagination_router.callback_query(
    FiltersState.base,
    PagionationVccData.filter(F.value==1)
)
async def increment_page(
        callback: CallbackQuery, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    data = await state.get_data()
    await state.update_data(page=data["page"]+1)
    meetings, meetings_count = await api_client.get_meetings(
        token, data["page"]+1,
        data["date_from"],
        data["date_to"],
        data["state"],
        data["filter"])
     
    print(meetings)
    #result = [refactor_meeting(meeting) for meeting in meetings]

    await callback.message.edit_text(
        #str([refactor_meeting(meeting) for meeting in meetings]),
        refactor_meetings(meetings), 
        reply_markup=get_filters_keyboard(meetings_count, data["page"]+1)
    )

@pagination_router.callback_query(
    FiltersState.base,
    PagionationVccData.filter(F.value==-1)
)
async def increment_page(
        callback: CallbackQuery, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    data = await state.get_data()
    await state.update_data(page=data["page"]-1)
    meetings, meetings_count = await api_client.get_meetings(
        token, data["page"]-1,
        data["date_from"],
        data["date_to"],
        data["state"],
        data["filter"])
    
    #result = [refactor_meeting(meeting) for meeting in meetings]

    await callback.message.edit_text(
        #str([refactor_meeting(meeting) for meeting in meetings]), 
        refactor_meetings(meetings), 
        reply_markup=get_filters_keyboard(meetings_count, data["page"]-1)
    )