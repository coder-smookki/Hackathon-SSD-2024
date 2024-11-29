from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.get_vcc import FilterVcc
from bot.core.api.api_vks import AsyncAPIClient
from bot.core.states.get_vcc import FiltersState
from bot.core.utils.get_vcc import refactor_meetings
from bot.keyboards.get_vcc import cancel_name_keyboard, get_filters_keyboard

filter_name_router = Router(name=__name__)


@filter_name_router.callback_query(
    FiltersState.base,
    FilterVcc.filter(F.name == "name"),  # TODO
)
async def filter_state_date(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(FiltersState.name)
    await callback.message.answer(
        "Введите текст для поиска",
        reply_markup=cancel_name_keyboard,
    )
    await callback.answer()


@filter_name_router.message(FiltersState.name)
async def get_filter_state_date(
    message: Message,
    state: FSMContext,
    api_client: AsyncAPIClient,
    token: str,
):
    data = await state.get_data()
    data["filter"]["filter"] = message.text
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
    await message.answer(
        refactor_meetings(meetings),
        reply_markup=get_filters_keyboard(meetings_count, 1),
    )
