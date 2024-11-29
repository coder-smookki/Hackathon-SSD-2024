from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.universal import YesNo
from bot.core.api.api_vks import AsyncAPIClient
from bot.handlers.create_vcc.formulations import END_CREATION_VKS
from bot.handlers.create_vcc.handlers.base_data import start_create
from bot.handlers.create_vcc.state import CreateVccState
from bot.keyboards.universal import back_menu_keyboard
from database.models import UserModel

check_data_vcc_router = Router(name=__name__)


@check_data_vcc_router.callback_query(
    CreateVccState.check_data, YesNo.filter(F.result == "Нет")
)
async def no_check_data(
    callback: CallbackQuery,
    state: FSMContext,
):
    """отбрасываем в самое начало"""
    await state.clear()
    await start_create(callback, state)


@check_data_vcc_router.callback_query(
    CreateVccState.check_data, YesNo.filter(F.result == "Да")
)
async def yes_check_data(
    callback: CallbackQuery,
    state: FSMContext,
    api_client: AsyncAPIClient,
    token: str,
    user: UserModel,
):
    """Делаем запрос на создание"""
    state_data = await state.get_data()
    data = await api_client.create_meeting(
        jwt_token=token,
        organizer_id=user.vcc_id,
        name_vks=state_data["name"],
        date_vks=state_data["date"],
        duration_vks=state_data["duration"],
        participants_count_vks=state_data["participants_count"],
        participants=state_data["participants"],
        backend=state_data["backend"],
        settings=state_data["settings"],
    )
    if data["status"] != 201:
        await callback.message.edit_text(
            "❌ Произошла ошибка. Попробуйте ещё раз.\n"
            + "Детали: "
            + str(data["data"]["detail"]),
            reply_markup=back_menu_keyboard,
        )
    else:
        await callback.message.edit_text(
            END_CREATION_VKS.format(
                permalink=data["data"]["permalink"],
                participants=[
                    participant["email"] for participant in data["data"]["participants"]
                ],
            ),
            reply_markup=back_menu_keyboard,
        )
