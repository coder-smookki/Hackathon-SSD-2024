from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.get_vcc import FilterVcc
from bot.core.api.api_vks import AsyncAPIClient
from bot.core.states.get_vcc import FiltersState
from bot.core.utils.get_vcc import refactor_meetings
from bot.core.utils.utils import is_valid_email
from bot.keyboards.get_vcc import cancel_user_keyboard, get_filters_keyboard

filter_user_router = Router(name=__name__)


@filter_user_router.callback_query(
    FiltersState.base, FilterVcc.filter(F.name == "user")
)
async def filter_user_date(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(FiltersState.user)
    await callback.message.edit_text(
        "Введите Имейл админа", reply_markup=cancel_user_keyboard
    )


@filter_user_router.message(FiltersState.user)
async def get_filter_user_date(
    message: Message, state: FSMContext, api_client: AsyncAPIClient, token: str
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
        token, 1, data["date_from"], data["date_to"], data["state"], data["filter"]
    )
    await message.answer(
        refactor_meetings(meetings),
        reply_markup=get_filters_keyboard(meetings_count, 1),
    )
