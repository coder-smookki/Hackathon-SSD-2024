from datetime import datetime, timedelta
import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards.universal import confirm_cancel_keyboard
from bot.keyboards.start import start_keyboard
from bot.callbacks.authorization import Authorization
from bot.callbacks.state import InStateData
from bot.core.utils.enums import Operation
from bot.core.api.api_vks import AsyncAPIClient


logger = logging.getLogger(__name__)
router_auth = Router(name=__name__)


class ExtractData(StatesGroup):
    """Установление состояний: login, password, confirm"""
    login = State()
    password = State()
    confirm_check_data = State() # Согласие на достоверность данных
    confirm_save_data = State() # Согласие на сохранение данных


@router_auth.callback_query(Authorization.filter(F.operation_auth == "authorization"))
async def send_email(callback: CallbackQuery, state: FSMContext) -> None:
    """Запрашиваем email у пользователя"""
    await callback.message.edit_text(text="Введите login:")
    await state.set_state(ExtractData.login)


@router_auth.message(ExtractData.login)
async def send_password(message: Message, state: FSMContext) -> None:
    """Сохраняем login и запрашиваем password"""
    await state.update_data(login=message.text)
    await message.answer("Введите password:")
    await state.set_state(ExtractData.password)


@router_auth.message(ExtractData.password)
async def save_password(message: Message, state: FSMContext) -> None:
    """Сохраняем password и предлагаем подтвердить действия"""
    await state.update_data(password=message.text)
    user_data = await state.get_data()
    user_info = f"Дogin: {user_data.get('login')}\nPassword: {user_data.get('password')}"

    await message.answer(
        text=f"Вы ввели следующие данные:\n{user_info}\n\nХотите подтвердить действия?",
        reply_markup=confirm_cancel_keyboard
    )
    await state.set_state(ExtractData.confirm_check_data)


@router_auth.callback_query(ExtractData.confirm_check_data,
                            InStateData.filter(F.action == Operation.CANCEL))
async def no_confirm_check_data(callback: CallbackQuery, state: FSMContext) -> None:
    """Пользователь отменил действия"""
    await callback.message.edit_text(
        text="Действие отменено", 
        reply_markup=start_keyboard
    )
    await state.clear()


@router_auth.callback_query(ExtractData.confirm_check_data,
                     InStateData.filter(F.action == Operation.CONFIRM))
async def confirm_save_data(callback: CallbackQuery, state: FSMContext) -> None:
    """Спрашиваем сохранить ли данные"""
    await state.update_data(confirm_check_data=True)

    await callback.message.edit_text(
        text=f"Хотите ли вы, сохранить данные в боте, для удобной авторизации?",
        reply_markup=confirm_cancel_keyboard
    )
    await state.set_state(ExtractData.confirm_save_data)


# нижнии функции можно объединить
@router_auth.callback_query(ExtractData.confirm_save_data,
                            InStateData.filter(F.action == Operation.CONFIRM))
async def yes_confirm_save_data(callback: CallbackQuery, state: FSMContext) -> None:
    """Пользователь согласился сохранить данные"""
    await state.update_data(confirm_save_data=True)
    user_data = await state.get_data()
    user_info = {
        "login": user_data.get("login"),
        "password": user_data.get("password"),
        "confirm_check_data": user_data.get("confirm_check_data"),
        "confirm_save_data": user_data.get("confirm_save_data")
    }
    try:
        token = await AsyncAPIClient().get_token(user_info["login"], user_info["password"])
    except Exception:
        await callback.message.edit_text(
            text="Данные неверны", 
            reply_markup=start_keyboard
        )
        await state.clear()
        return
    await state.update_data(token=token)
    await state.update_data(
        expired_time=datetime.now()+timedelta(hours=3, minutes=45)
    ) # сдвиг в 15 минут, чтобы мы были уверены что токен свежий
    logger.info(f"Собранные данные пользователя: {user_info}")
    
    await callback.message.edit_text(text=f"Данные успешно сохранены: {user_info}")
    await state.set_state(None)


@router_auth.callback_query(ExtractData.confirm_save_data,
                            InStateData.filter(F.action == Operation.CANCEL))
async def no_confirm_save_data(callback: CallbackQuery, state: FSMContext) -> None:
    """Пользователь согласился сохранить данные"""
    await state.update_data(confirm_save_data=False)
    user_data = await state.get_data()
    user_info = {
        "login": user_data.get("login"),
        "password": user_data.get("password"),
        "confirm_check_data": user_data.get("confirm_check_data"),
        "confirm_save_data": user_data.get("confirm_save_data")
    }

    try:
        token = await AsyncAPIClient().get_token(user_info["login"], user_info["password"])
    except Exception:
        await callback.message.edit_text(
            text="Данные неверны", 
            reply_markup=start_keyboard
        )
        await state.clear()
        return
    await state.update_data(token=token)
    await state.update_data( # TODO сунуть имя куда-то
        expired_time=datetime.now()+timedelta(hours=3, minutes=45)
    ) # сдвиг в 15 минут, чтобы мы были уверены что токен свежий

    logger.info(f"Собранные данные пользователя: {user_info}")
    
    await callback.message.edit_text(
        text=f"Данные успешно сохранены: {user_info}",
        # TODO сделать клаву
    )
    await state.set_state(None)