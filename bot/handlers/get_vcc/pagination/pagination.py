from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.callbacks.get_vcc import PagionationVccData
from bot.core.api.api_vks import AsyncAPIClient
from bot.handlers.get_vcc.state import FiltersState
from bot.core.utils.get_vcc import refactor_meetings
from bot.keyboards.get_vcc import get_filters_keyboard

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
     
    await callback.message.edit_text(
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
    
    await callback.message.edit_text(
        refactor_meetings(meetings), 
        reply_markup=get_filters_keyboard(meetings_count, data["page"]-1)
    )