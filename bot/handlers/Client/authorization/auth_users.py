from typing import Any, Final
from aiogram import Router, F, BaseMiddleware
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import TelegramObject

from callbacks.client import ProfileAuthorization

import logging

logger = logging.getLogger(__name__)
router_auth = Router(name=__name__)


class ExtractData(StatesGroup):
    """Установление состояний: email, login, password, confirm"""
    email = State()
    login = State()
    password = State()
    confirm = State()


@router_auth.callback_query(ProfileAuthorization.filter(F.operation_auth == "authorization"))
async def send_email(callback: CallbackQuery, state: FSMContext) -> None:
    """Запрашиваем email у пользователя"""
    await callback.message.answer("Введите email:")
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

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="confirm_yes"),
            InlineKeyboardButton(text="Нет", callback_data="confirm_no")
        ]
    ])

    await message.answer(
        text=f"Вы ввели следующие данные:\n{user_info}\n\nХотите подтвердить действия?",
        reply_markup=buttons
    )
    await state.set_state(ExtractData.confirm)


@router_auth.callback_query(F.data == "confirm_yes")
async def confirm_yes(callback: CallbackQuery, state: FSMContext) -> None:
    """Пользователь подтвердил действия"""
    user_data = await state.get_data()
    user_info = {
        "email": user_data.get("email"),
        "login": user_data.get("login"),
        "password": user_data.get("password"),
    }
    logger.info(f"Собранные данные пользователя: {user_info}")
    await callback.message.edit_text(text=f"Данные успешно сохранены: {user_info}")
    await state.clear()


@router_auth.callback_query(F.data == "confirm_no")
async def confirm_no(callback: CallbackQuery, state: FSMContext) -> None:
    """Пользователь отменил действия"""
    await callback.message.edit_text(text="Действие отменено. Попробуйте снова.")
    await state.clear()
