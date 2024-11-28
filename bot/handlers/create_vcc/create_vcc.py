from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.callbacks.create_vcc import (
    StartCreateVcc, 
    ChooseBackendVcc,
    ChooseBuilding,
    ChooseRoom
)
from bot.callbacks.universal import YesNo
from bot.callbacks.state import InStateData
from bot.handlers.create_vcc.state import (
    CreateVccState,
    CiscoSettingsState,
    VinteoSettingsState,
    ExternalSettingsState
)
from bot.keyboards.create_vcc import (
    choose_backend_keyboard, 
    create_choose_building_keyboard,
    create_choose_room_keyboard
)
from bot.keyboards.universal import yes_no_keyboard, cancel_state_keyboard
from bot.core.utils.enums import Operation
from bot.core.api.api_vks import AsyncAPIClient
from bot.core.utils.utils import is_valid_email
from database.models import UserModel


create_vcc_router = Router(name=__name__)


@create_vcc_router.callback_query(StartCreateVcc.filter())
async def start_create(
        callback: CallbackQuery, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    """ Старт создания, запрос имени """
    await state.set_state(CreateVccState.name)
    await callback.message.edit_text("start create vcc.\n введите название")


@create_vcc_router.message(CreateVccState.name)
async def get_name(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение имени, запрос даты проведения """
    await state.update_data(name=message.text)
    await state.set_state(CreateVccState.date)
    await message.answer("введите дату в формате yyyy mm dd hh mm (год месяц день час минута)\n2024 11 28 10 10")


@create_vcc_router.message(CreateVccState.date)
async def get_date(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение запрос даты проведения, запрос времени мероприятия """
    try:
        update_data = (datetime.strptime(message.text, "%Y %m %d %H %M") - timedelta(hours=5)).isoformat()
    except Exception:
        await message.answer("неверная дата")
        return

    await state.update_data(date=update_data)
    await state.set_state(CreateVccState.duration)
    await message.answer("введите продолжительность в минутах")


@create_vcc_router.message(CreateVccState.duration)
async def get_duration(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение времени мероприятия, запрос максимального количества """
    try:
        data = int(message.text)
    except ValueError:
        await message.answer("это не число")
        return
    await state.update_data(duration=data)
    await state.set_state(CreateVccState.participants_count_vks)
    await message.answer("введите макс количество людей")


@create_vcc_router.message(CreateVccState.participants_count_vks)
async def get_participants_count(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение максимального количества, запрос backend """
    try:
        data = int(message.text)
    except ValueError:
        await message.answer("это не число")
        return
    await state.update_data(participants_count=data)
    await state.set_state(CreateVccState.backend)
    await message.answer(
        "Выберите тип", 
        reply_markup=choose_backend_keyboard
    )



@create_vcc_router.callback_query(
    CreateVccState.backend, 
    ChooseBackendVcc.filter(F.name == "cisco")
)
async def start_get_cisco_settings(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    """ сохранение backend, запрос is_microphone_on """
    await state.update_data(backend = "cisco")
    await state.set_state(CiscoSettingsState.is_microphone_on)
    await callback.message.edit_text(
        text = "Включать ли микрофон обязятально?",
        reply_markup=yes_no_keyboard
    )

@create_vcc_router.callback_query(
    CiscoSettingsState.is_microphone_on,
    YesNo.filter()
)
async def start_get_cisco_settings(
        callback: CallbackQuery, 
        callback_data: YesNo,
        state: FSMContext,
    ):
    """ сохранение is_microphone_on, запрос is_video_on """
    await state.update_data(is_microphone_on = callback_data.result=="Да")
    await state.set_state(CiscoSettingsState.is_video_on)
    await callback.message.edit_text(
        text = "Включать ли видео обязательно?",
        reply_markup=yes_no_keyboard
    )

@create_vcc_router.callback_query(
    CiscoSettingsState.is_video_on,
    YesNo.filter()
)
async def start_get_cisco_settings(
        callback: CallbackQuery, 
        callback_data: YesNo,
        state: FSMContext,
    ):
    """ сохранение is_video_on, запрос is_waiting_room_enabled """
    await state.update_data(is_video_on = callback_data.result=="Да")
    await state.set_state(CiscoSettingsState.is_waiting_room_enabled)
    await callback.message.edit_text(
        text = "Включать ли ожидание что-то там?",
        reply_markup=yes_no_keyboard
    )

@create_vcc_router.callback_query(
    CiscoSettingsState.is_waiting_room_enabled,
    YesNo.filter()
)
async def start_get_cisco_settings(
        callback: CallbackQuery, 
        callback_data: YesNo,
        state: FSMContext,
    ):
    """ сохранение is_waiting_room_enabled, запрос need_video_recording """
    await state.update_data(is_waiting_room_enabled = callback_data.result=="Да")
    await state.set_state(CiscoSettingsState.need_video_recording)
    await callback.message.edit_text(
        text = "Включать ли видео запись?",
        reply_markup=yes_no_keyboard
    )

@create_vcc_router.callback_query(
    CiscoSettingsState.need_video_recording,
    YesNo.filter()
)
async def start_get_cisco_settings(
        callback: CallbackQuery, 
        callback_data: YesNo,
        state: FSMContext,
    ):
    """ сохранение need_video_recording, запрос на проверку данных """
    data = await state.get_data()
    await state.update_data(settings = {
        "isMicrophoneOn": data["is_microphone_on"],
        "isVideoOn": data["is_video_on"],
        "isWaitingRoomEnabled": data["is_waiting_room_enabled"],
        "needVideoRecording": callback_data.result=="Да",
    })

    await state.set_state(CreateVccState.participants)
    await state.update_data(participants=[])
    await callback.message.answer(
        "Вводите имейлы пользователей, или нажмайте сансел", 
        reply_markup=cancel_state_keyboard
    )



@create_vcc_router.callback_query(
    CreateVccState.backend, 
    ChooseBackendVcc.filter(F.name == "external")
)
async def start_get_external_settings(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    """ сохранение backend, запрос external_url """
    await state.update_data(backend = "external")
    await state.set_state(ExternalSettingsState.external_url)
    await callback.message.edit_text(
        text = "введите ссылку",
    )

@create_vcc_router.message(ExternalSettingsState.external_url)
async def start_get_external_settings(
        message: Message, 
        state: FSMContext,
    ):
    """ сохранение external_url, запрос на проверку данных """
    await state.update_data(settings = {
        "externalUrl": message.text
    })

    await state.set_state(CreateVccState.participants)
    await state.update_data(participants=[])
    await message.answer(
        "Вводите имейлы пользователей, или нажмайте сансел", 
        reply_markup=cancel_state_keyboard
    )



@create_vcc_router.callback_query(
    CreateVccState.backend, 
    ChooseBackendVcc.filter(F.name == "vinteo")
)
async def start_get_external_settings(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    """ сохранение backend, запрос need_video_recording """
    await state.update_data(backend = "vinteo")
    await state.set_state(VinteoSettingsState.need_video_recording)
    await callback.message.edit_text(
        text = "Видео запись заказывали?",
        reply_markup=yes_no_keyboard
    )

@create_vcc_router.callback_query(
    VinteoSettingsState.need_video_recording,
    YesNo.filter()
)
async def start_get_external_settings(
        callback: CallbackQuery, 
        callback_data: YesNo,
        state: FSMContext,
    ):
    """ сохранение need_video_recording, запрос на проверку данных """
    await state.update_data(settings = {
        "needVideoRecording": callback_data.result=="Да"
    })
    await state.set_state(CreateVccState.participants)
    await state.update_data(participants=[])
    await callback.message.answer(
        "Вводите имейлы пользователей, или нажмайте сансел", 
        reply_markup=cancel_state_keyboard
    )
    



@create_vcc_router.message(CreateVccState.participants)
async def get_participants(
        message: Message, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
    ):
    if not is_valid_email(message.text):
        await message.answer("это не имейл", reply_markup=cancel_state_keyboard)
        return
    user_data = await api_client.get_user(token, message.text)
    if not user_data["data"]["data"]:
        await message.answer("этого юзера нету в бд", reply_markup=cancel_state_keyboard)
        return

    data = await state.get_data()
    data["participants"].append({"id": user_data["data"]["data"][0]["id"]})
    await message.answer("добавлено", reply_markup=cancel_state_keyboard)


@create_vcc_router.callback_query(
        CreateVccState.participants, 
        InStateData.filter(F.action == Operation.CANCEL)
)
async def cancel_participants(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    await state.set_state(CreateVccState.set_room)
    await callback.message.edit_text(
        text = "комнату хотим?",
        reply_markup=yes_no_keyboard
    )


# может стоит объединить проверку даты?
@create_vcc_router.callback_query(
        CreateVccState.set_room,
        YesNo.filter(F.result == "Нет")
)
async def no_set_room(
        callback: CallbackQuery, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str,
        user: UserModel
    ): 
    await state.set_state(CreateVccState.check_data)
    state_data = await state.get_data()
    data = dict(
        jwt_token=token, # от тут не нужен
        organizer_id=user.vcc_id,
        name_vks=state_data["name"],
        date_vks=state_data["date"],
        duration_vks=state_data["duration"],
        participants_count_vks=state_data["participants_count"],
        participants=[{"email": "hantaton8.h@mail.ru"}],
        backend=state_data["backend"],
        settings=state_data["settings"]
    )
    await callback.message.edit_text(
        text = "данные корректны? \n" + str(data),  # TODO сунуть данные для проверка
        reply_markup=yes_no_keyboard
    )
    
@create_vcc_router.callback_query(
        CreateVccState.set_room,
        YesNo.filter(F.result == "Да")
)
async def yes_set_room(
        callback: CallbackQuery, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str,
        user: UserModel
    ):
    await state.set_state(CreateVccState.building)
    data = await api_client.get_buildings(token)
    await callback.message.edit_text(
        "Выберите здание", 
        reply_markup=create_choose_building_keyboard(data["data"]["data"])
    )

@create_vcc_router.callback_query(
        CreateVccState.building,
        ChooseBuilding.filter()
)
async def get_building(
        callback: CallbackQuery, 
        callback_data: ChooseBuilding,
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str,
        user: UserModel
    ):
    await state.set_state(CreateVccState.room)
    data = await api_client.get_rooms(token, callback_data.id)
    await callback.message.edit_text(
        "Выберите комнату", 
        reply_markup=create_choose_room_keyboard(data["data"]["data"])
    )

@create_vcc_router.callback_query(
        CreateVccState.room,
        ChooseRoom.filter()
)
async def get_room(
        callback: CallbackQuery, 
        callback_data: ChooseRoom,
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str,
        user: UserModel
    ):
    await state.set_state(CreateVccState.check_data)
    state_data = await state.get_data()
    data = dict(
        jwt_token=token, # от тут не нужен
        organizer_id=user.vcc_id,
        name_vks=state_data["name"],
        date_vks=state_data["date"],
        duration_vks=state_data["duration"],
        participants_count_vks=state_data["participants_count"],
        participants=state_data["participants"],
        backend=state_data["backend"],
        settings=state_data["settings"],
        place=callback_data.id
    )
    await callback.message.edit_text(
        text = "данные корректны? \n" + str(data),  # TODO сунуть данные для проверка
        reply_markup=yes_no_keyboard
    )
    




@create_vcc_router.callback_query(
        CreateVccState.check_data,
        YesNo.filter(F.result == "Нет")
)
async def no_check_data(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    """ отбрасываем в самое начало """
    await state.clear()
    await start_create(callback, state)

@create_vcc_router.callback_query(
        CreateVccState.check_data,
        YesNo.filter(F.result == "Да")
)
async def yes_check_data(
        callback: CallbackQuery, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str,
        user: UserModel
    ):
    """ Делаем запрос на создание """
    state_data = await state.get_data()
    data = await api_client._create_meeting(
        jwt_token=token,
        organizer_id=user.vcc_id,
        name_vks=state_data["name"],
        date_vks=state_data["date"],
        duration_vks=state_data["duration"],
        participants_count_vks=state_data["participants_count"],
        participants=state_data["participants"],
        backend=state_data["backend"],
        settings=state_data["settings"]
    )
    if data["status"] != 201:
        await callback.message.edit_text("не получилось "+str(data["data"]))
    else:
        await callback.message.edit_text("Все круттттттаааааааа "+str(data["data"]))