from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.handlers.get_vcc.state import GetVccState, FiltersState
from bot.handlers.get_vcc.utils import refactor_meeting
from bot.core.api.api_vks import AsyncAPIClient
from bot.keyboards.get_vcc import get_filters_keyboard
from bot.callbacks.get_vcc import StartGetVcc



""" 
здесь происходит старт и береться все необходимое для запроса
(Промежуток дат)
(datetime.strptime(message.text, "%Y %m %d %H %M") - timedelta(hours=5)).isoformat()
"""

start_router = Router(name=__name__)

@start_router.callback_query(StartGetVcc.filter(F.back_menu == "start_create_vcc"))
async def start_get(
        message: Message, 
        state: FSMContext,
    ):
    """ Старт создания, запрос даты от """
    await state.set_state(GetVccState.date_from)
    await message.answer(
        "start get vcc.\n \
        введите дату НАЧАЛА в формате yyyy mm dd hh mm \
        (год месяц день час минута)\n \
        2024 11 28 10 10"
    )


@start_router.message(GetVccState.date_from)
async def get_date(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение даты от, запрос даты до """
    try:
        update_data = (datetime.strptime(message.text, "%Y %m %d %H %M") - timedelta(hours=5)).isoformat()
    except Exception:
        await message.answer("неверная дата")
        return
    await state.update_data(date_from=update_data)
    
    await state.set_state(GetVccState.date_to)
    await message.answer(
        "введите дату КОНЦА в формате yyyy mm dd hh mm \
        (год месяц день час минута)\n \
        2024 11 28 10 10"
    )

@start_router.message(GetVccState.date_to)
async def get_date(
        message: Message, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    """ сохранение даты до, перенос в меню фильтров """
    try:
        update_data = (datetime.strptime(message.text, "%Y %m %d %H %M") - timedelta(hours=5)).isoformat()
    except Exception:
        await message.answer("неверная дата")
        return
    await state.update_data(
        date_to=update_data,
        state="booked",
        page=1,
        filter={}
    )

    data = await state.get_data()
    meetings, meetings_count = await api_client.get_meetings(
        token, data["page"], 
        data["date_from"], 
        data["date_to"], 
        "booked"
    )
    print(meetings, meetings_count)
    result = [refactor_meeting(meeting) for meeting in meetings]
    keyboard = get_filters_keyboard 
    await message.answer(
        str(result), 
        reply_markup=get_filters_keyboard(meetings_count, 1)
    )
    await state.set_state(FiltersState.base)

    