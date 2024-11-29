from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.create_vcc import StopAddUser
from bot.core.api.api_vks import AsyncAPIClient
from bot.core.utils.utils import is_valid_email
from bot.handlers.create_vcc.state import CreateVccState
from bot.keyboards.create_vcc import stop_add_users
from bot.keyboards.universal import yes_no_keyboard

participants_vcc_router = Router(name=__name__)


@participants_vcc_router.message(CreateVccState.participants)
async def get_participants(
    message: Message, state: FSMContext, api_client: AsyncAPIClient, token: str
):
    if not is_valid_email(message.text):
        await message.answer("❌ Это не email!", reply_markup=stop_add_users)
        return
    user_data = await api_client.get_user(token, message.text)
    if not user_data["data"]["data"]:
        await message.answer("❌ Этого пользователя нету", reply_markup=stop_add_users)
        return
    data = await state.get_data()
    if {"id": user_data["data"]["data"][0]["id"]} in data["participants"]:
        await message.answer(
            "❌ Этот пользователь уже добавлен", reply_markup=stop_add_users
        )
        return
    data["participants"].append({"id": user_data["data"]["data"][0]["id"]})
    await message.answer("✅ Добавлен", reply_markup=stop_add_users)


@participants_vcc_router.callback_query(
    CreateVccState.participants, StopAddUser.filter()
)
async def cancel_participants(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(CreateVccState.set_room)
    await callback.message.edit_text(
        text="🔒 Хотите ли вы указать помещение ВКС?", reply_markup=yes_no_keyboard
    )
