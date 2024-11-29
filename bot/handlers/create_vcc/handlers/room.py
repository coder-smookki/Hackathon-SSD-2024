from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.create_vcc import ChooseBuilding, ChooseRoom
from bot.callbacks.universal import YesNo
from bot.core.api.api_vks import AsyncAPIClient
from bot.handlers.create_vcc.formulations import (
    CREATION_VKS_CISCO,
    CREATION_VKS_EXTERNAL,
    CREATION_VKS_VINTEO,
)
from bot.handlers.create_vcc.state import CreateVccState
from bot.keyboards.create_vcc import (
    create_choose_building_keyboard,
    create_choose_room_keyboard,
)
from bot.keyboards.universal import yes_no_keyboard
from database.models import UserModel

room_vcc_router = Router(name=__name__)


@room_vcc_router.callback_query(CreateVccState.set_room, YesNo.filter(F.result == "Да"))
async def yes_set_room(
    callback: CallbackQuery,
    state: FSMContext,
    api_client: AsyncAPIClient,
    token: str,
):
    await state.set_state(CreateVccState.building)
    data = await api_client.get_buildings(token)
    await callback.message.edit_text(
        "🔒 Выберите здание, где будет ВКС.",
        reply_markup=create_choose_building_keyboard(data["data"]["data"]),
    )


@room_vcc_router.callback_query(CreateVccState.building, ChooseBuilding.filter())
async def get_building(
    callback: CallbackQuery,
    callback_data: ChooseBuilding,
    state: FSMContext,
    api_client: AsyncAPIClient,
    token: str,
):
    await state.set_state(CreateVccState.room)
    data = await api_client.get_rooms(token, callback_data.id)
    await callback.message.edit_text(
        "🔒 Выберите комнату для ВКС.",
        reply_markup=create_choose_room_keyboard(data["data"]["data"]),
    )


@room_vcc_router.callback_query(CreateVccState.room, ChooseRoom.filter())
async def get_room(
    callback: CallbackQuery,
    callback_data: ChooseRoom,
    state: FSMContext,
    api_client: AsyncAPIClient,
    token: str,
    user: UserModel,
):
    await state.set_state(CreateVccState.check_data)
    state_data = await state.get_data()
    data = dict(
        jwt_token=token,  # от тут не нужен
        organizer_id=user.vcc_id,
        name_vks=state_data["name"],
        date_vks=state_data["date"],
        duration_vks=state_data["duration"],
        participants_count_vks=state_data["participants_count"],
        participants=state_data["participants"],
        backend=state_data["backend"],
        settings=state_data["settings"],
        place=callback_data.id,
    )
    if state_data["backend"] == "cisco":
        result = CREATION_VKS_CISCO.format(
            name=data["name_vks"],
            participantsCount=data["participants_count_vks"],
            startedAt=data["date_vks"],
            duration=data["duration_vks"],
            backend=data["backend"],
            isMicrophoneOn="Да" if bool(data["settings"]["isMicrophoneOn"]) else "Нет",
            isVideoOn="Да" if bool(data["settings"]["isVideoOn"]) else "Нет",
            isWaitingRoomEnabled=(
                "Да" if bool(data["settings"]["isWaitingRoomEnabled"]) else "Нет"
            ),
            needVideoRecording=(
                "Да" if bool(data["settings"]["needVideoRecording"]) else "Нет"
            ),
        )
    elif state_data["backend"] == "external":
        result = CREATION_VKS_EXTERNAL.format(
            name=data["name_vks"],
            participantsCount=data["participants_count_vks"],
            startedAt=data["date_vks"],
            duration=data["duration_vks"],
            backend=data["backend"],
            externalUrl=data["settings"]["externalUrl"],
        )
    if state_data["backend"] == "vinteo":
        result = CREATION_VKS_VINTEO.format(
            name=data["name_vks"],
            participantsCount=data["participants_count_vks"],
            startedAt=data["date_vks"],
            duration=data["duration_vks"],
            backend=data["backend"],
            needVideoRecording=(
                "Да" if bool(data["settings"]["needVideoRecording"]) else "Нет"
            ),
        )
    await callback.message.edit_text(text=result, reply_markup=yes_no_keyboard)
