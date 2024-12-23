from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.logout import Logout
from bot.core.api.api_vks import AsyncAPIClient
from bot.keyboards.start import start_keyboard
from database.models import UserModel
from database.repositories import UserAlchemyRepo

logout_router = Router(name=__name__)


@logout_router.callback_query(Logout.filter())
async def cmd_logout(
    callback: CallbackQuery,
    state: FSMContext,
    api_client: AsyncAPIClient,
    user_repo: UserAlchemyRepo,
    user: UserModel,
    token: str,
):
    await api_client.auth_logout(token=token)
    await state.clear()
    await user_repo.delete(user.tg_id)
    await callback.message.edit_text(
        text="Вы успешно вышли из системы.",
        reply_markup=start_keyboard,
    )
