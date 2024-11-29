import logging
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.authorization import Authorization
from bot.callbacks.state import InStateData
from bot.core.api.api_vks import AsyncAPIClient, AuthorizationException
from bot.core.models import User
from bot.core.states.auth import ExtractData
from bot.core.utils.enums import Operation
from bot.core.utils.jwt import get_expired_time_token, parse_token
from bot.core.utils.utils import is_valid_email
from bot.handlers.menu.main_menu import cmd_menu
from bot.keyboards.start import start_keyboard
from bot.keyboards.universal import confirm_cancel_keyboard
from database.repositories import UserAlchemyRepo

logger = logging.getLogger(__name__)
auth_router = Router(name=__name__)


@auth_router.callback_query(Authorization.filter(F.operation_auth == "authorization"))
async def send_email(callback: CallbackQuery, state: FSMContext) -> None:
    """Запрашиваем email у пользователя"""
    await callback.message.edit_text(
        text="✉️ Введите почту:\n\n⚙️ Пример: hantaton10.h@mail.ru"
    )
    await state.set_state(ExtractData.email)


@auth_router.message(ExtractData.email)
async def send_password(message: Message, state: FSMContext) -> None:
    """Сохраняем email и запрашиваем password"""
    if not is_valid_email(message.text):
        await message.answer("❌ Это не email!")
        return
    await state.update_data(email=message.text)
    await message.answer("🔑 Введите пароль:\n\n⚙️ Пароль: 14Jiuqnr1sWWvo6G")
    await state.set_state(ExtractData.password)


@auth_router.message(ExtractData.password)
async def save_password(message: Message, state: FSMContext) -> None:
    """Сохраняем password и предлагаем подтвердить действия"""
    await state.update_data(password=message.text)
    user_data = await state.get_data()
    user_info = (
        f"✉️ Почта: {user_data.get('email')}\n🔑 Пароль: {user_data.get('password')}"
    )

    await message.answer(
        text=f"💾 Вы ввели следующие данные:\n\n{user_info}\n\n❗ Хотите подтвердить действия?",
        reply_markup=confirm_cancel_keyboard,
    )
    await state.set_state(ExtractData.confirm_check_data)


@auth_router.callback_query(
    ExtractData.confirm_check_data, InStateData.filter(F.action == Operation.CANCEL)
)
async def no_confirm_check_data(callback: CallbackQuery, state: FSMContext) -> None:
    """Пользователь отменил действия"""
    await callback.message.edit_text(
        text="❗ Действие отменено.", reply_markup=start_keyboard
    )
    await state.clear()


@auth_router.callback_query(ExtractData.confirm_check_data, InStateData.filter())
async def yes_confirm_check_data(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: InStateData,
    user_repo: UserAlchemyRepo,
    api_client: AsyncAPIClient,
) -> None:
    """Финальный этап, получение токена, сохранение данных с него в бд"""
    await state.update_data(
        confirm_check_data=callback_data.action == Operation.CONFIRM
    )
    user_data = await state.get_data()
    user_info = {
        "email": user_data.get("email"),
        "confirm_check_data": user_data.get("confirm_check_data"),
    }

    try:
        auth_data = await api_client.auth_login(
            user_data["email"], user_data["password"]
        )
    except AuthorizationException:
        await callback.message.edit_text(
            text="❌ Данные неверны!", reply_markup=start_keyboard
        )
        await state.clear()
        return
    vcc_user = auth_data["user"]

    # сброс данных
    await state.update_data(email="*")
    await state.update_data(password="*")

    token_data = parse_token(auth_data["token"])
    token_expired_at = get_expired_time_token(auth_data["token"])
    refresh_token = token_data["refresh_token"]
    refresh_token_expired_at = get_expired_time_token(refresh_token)

    if vcc_user["birthday"] is not None:
        user_birthday = datetime.strptime(vcc_user["birthday"], "%Y-%m-%d").date()
    else:
        user_birthday = None
    user = User(
        tg_id=callback.from_user.id,
        login=vcc_user["login"],
        email=user_info["email"],
        token=auth_data["token"],
        token_expired_at=token_expired_at,
        refresh_token=refresh_token,
        refresh_token_expired_at=refresh_token_expired_at,
        vcc_id=vcc_user["id"],
        first_name=vcc_user["firstName"],
        last_name=vcc_user["lastName"],
        midle_name=vcc_user["middleName"],
        birthday=user_birthday,
        phone=vcc_user["phone"],
    )
    await user_repo.create(user)

    logger.info(f"📎 Собранные данные пользователя: {user.model_dump()}")

    await callback.message.edit_text(
        text="✅ Данные успешно сохранены.",
    )
    await cmd_menu(message=callback.message, state=state)
    await state.set_state(None)
