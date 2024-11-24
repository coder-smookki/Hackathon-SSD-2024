from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State

from bot.callbacks.client import CallbackData
from bot.callbacks.client import ProfileAuthorization
router_auth = Router(name=__name__)


class ExtractData(StatesGroup):
    '''Устанвление состояний: email, login, password'''
    email = State()
    login = State()
    password = State()


@router_auth.callback_query(ProfileAuthorization.filter(F.operation_auth == "authorization"))
async def send_emil(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer("Введите email:")
    await state.set_state(ExtractData.email)


@router_auth.message(ExtractData.email)
async def send_login(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await message.answer("Введите login:")
    await state.set_state(ExtractData.login)


@router_auth.message(ExtractData.login)
async def send_login(message: Message, state: FSMContext) -> None:
    await state.update_data(login=message.text)
    await message.answer("Введите password:")
    await state.set_state(ExtractData.password)


@router_auth.message(ExtractData.password)
async def authorization(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    await message.answer(text=f'Данные успешно сохранены')

    data = await state.get_data()
    # await message.answer(data['email'])
    user_info = {
        "email": data['email'],
        "login": data['login'],
        "password": data['password']
    }
    await message.answer(text=f"{user_info}")
#