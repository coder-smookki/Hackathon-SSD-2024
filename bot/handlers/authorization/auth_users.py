from typing import Any, Final
from aiogram import Router, F, BaseMiddleware
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import TelegramObject
from bot.keyboards.universal import confirm_cancel_keyboard
from bot.callbacks.authorization import Authorization
from bot.callbacks.state import InStateData
from bot.core.utils.enums import Operation

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)
router_auth = Router(name=__name__)


class ExtractData(StatesGroup):
    """Установление состояний: email, login, password, confirm"""
    email = State()
    login = State()
    password = State()
    confirm = State()



# @router_auth.callback_query(ProfileAuthorization.filter(F.operation_auth == "authorization"))
# async def IsAuthYet(callback: CallbackQuery, data: Dict[str, Any]):
#     await callback.answer("Вы уже авторизированы")


@router_auth.callback_query(Authorization.filter(F.operation_auth == "authorization"))
async def send_email(callback: CallbackQuery, state: FSMContext) -> None:
    """Запрашиваем email у пользователя"""
    await callback.message.edit_text(text="Введите email:")
    await state.set_state(ExtractData.email)


@router_auth.message(ExtractData.email)
async def send_login(message: Message, state: FSMContext) -> None:
    """Сохраняем email и запрашиваем login"""
    await state.update_data(email=message.text)
    await message.answer("Введите login:")
    await state.set_state(ExtractData.login)


@router_auth.message(ExtractData.login)
async def send_password(message: Message, state: FSMContext) -> None:
    """Сохраняем login и запрашиваем password"""
    await state.update_data(login=message.text)
    await message.answer("Введите password:")
    await state.set_state(ExtractData.password)


@router_auth.message(ExtractData.password)
async def confirm_action(message: Message, state: FSMContext) -> None:
    """Сохраняем password и предлагаем подтвердить действия"""
    await state.update_data(password=message.text)
    user_data = await state.get_data()
    user_info = f"Email: {user_data.get('email')}\nLogin: {user_data.get('login')}\nPassword: {user_data.get('password')}"

    await message.answer(
        text=f"Вы ввели следующие данные:\n{user_info}\n\nХотите подтвердить действия?",
        reply_markup=confirm_cancel_keyboard
    )
    await state.set_state(ExtractData.confirm)


@router_auth.callback_query(ExtractData.confirm,
                            InStateData.filter(F.action == Operation.CONFIRM))
async def confirm_yes(callback: CallbackQuery, state: FSMContext) -> None:
    """Пользователь подтвердил действия"""
    await state.update_data(confirm=True)
    user_data = await state.get_data()
    user_info = {
        "email": user_data.get("email"),
        "login": user_data.get("login"),
        "password": user_data.get("password"),
        "confirm": user_data.get("confirm"),
    }
    logger.info(f"Собранные данные пользователя: {user_info}")
    await callback.message.edit_text(text=f"Данные успешно сохранены: {user_info}")
    await state.clear()


@router_auth.callback_query(ExtractData.confirm,
                            InStateData.filter(F.action == Operation.CANCEL))
async def confirm_no(callback: CallbackQuery, state: FSMContext) -> None:
    """Пользователь отменил действия"""
    await callback.message.edit_text(text="Действие отменено")
    await state.clear()