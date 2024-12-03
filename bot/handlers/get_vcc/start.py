from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.get_vcc import StartGetVcc
from bot.core.api.api_vks import AsyncAPIClient
from bot.core.states.get_vcc import FiltersState, GetVccState
from bot.core.utils.get_vcc import refactor_meetings
from bot.core.utils.utils import parse_datetime
from bot.keyboards.get_vcc import get_filters_keyboard
from bot.keyboards.universal import back_menu_keyboard

""" 
здесь происходит старт и береться промежуток дат для запроса
"""

start_router = Router(name=__name__)


@start_router.callback_query(StartGetVcc.filter())
async def start_get(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Старт создания, запрос даты от"""
    await state.set_state(GetVccState.date_from)
    await callback.message.edit_text(
        "Введите дату НАЧАЛА в формате ДД ММ ГГГГ ЧЧ ММ (день месяц год час минута)\n 28 11 2024 10 10",
        reply_markup=back_menu_keyboard,
    )


@start_router.message(GetVccState.date_from)
async def get_date(message: Message, state: FSMContext):
    """сохранение даты от, запрос даты до"""
    try:
        update_data = parse_datetime(message.text)
    except Exception:
        await message.answer("неверная дата")
        return
    await state.update_data(date_from=update_data)

    await state.set_state(GetVccState.date_to)
    await message.answer(
        "Введите дату КОНЦА в формате ДД ММ ГГГГ ЧЧ ММ (день месяц год час минута) \n 28 11 2024 10 10",
        reply_markup=back_menu_keyboard,
    )


@start_router.message(GetVccState.date_to)
async def get_date(
    message: Message,
    state: FSMContext,
    api_client: AsyncAPIClient,
    token: str,
):
    """сохранение даты до, перенос в меню фильтров"""
    try:
        update_data = parse_datetime(message.text)
    except Exception:
        await message.answer("Неверная дата")
        return

    await state.update_data(date_to=update_data, state="booked", page=1, filter={})
    data = await state.get_data()
    print(data)
    meetings, meetings_count = await api_client.get_meetings(
        token,
        data["page"],
        data["date_from"],
        data["date_to"],
        "booked",
    )
    print(meetings)
    #meetings
    await message.answer(
        refactor_meetings(meetings),
        reply_markup=get_filters_keyboard(meetings_count, 1),
    )
    await state.set_state(FiltersState.base)
