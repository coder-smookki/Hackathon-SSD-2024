from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.callbacks.create_vcc import (
    StartCreateVcc, 
    ChooseBackendVcc,
    ChooseBuilding,
    ChooseRoom,
    StopAddUser
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
    stop_add_users,
    create_choose_building_keyboard,
    create_choose_room_keyboard
)
from bot.keyboards.universal import yes_no_keyboard, back_menu_keyboard
from bot.core.utils.enums import Operation
from bot.core.utils.utils import parse_datetime
from bot.core.api.api_vks import AsyncAPIClient
from bot.core.utils.utils import is_valid_email
from database.models import UserModel
from bot.handlers.create_vcc.formulations import (
    CREATION_VKS_CISCO, 
    CREATION_VKS_EXTERNAL,
    CREATION_VKS_VINTEO,
    END_CREATION_VKS
)


create_vcc_router = Router(name=__name__)


@create_vcc_router.callback_query(StartCreateVcc.filter())
async def start_create(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    """ Старт создания, запрос имени """
    await state.set_state(CreateVccState.name)
    await callback.message.edit_text("📋 Введите название ВКС:")
    await callback.message.edit_reply_markup(reply_markup=back_menu_keyboard)


@create_vcc_router.message(CreateVccState.name)
async def get_name(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение имени, запрос даты проведения """
    await state.update_data(name=message.text)
    await state.set_state(CreateVccState.date)
    await message.answer("⌛ Введите дату в формате ДД ММ ГГГГ ЧЧ ММ (год месяц день час минута):\n\n⚙️ Пример: 28 11 2024 10 10",
        reply_markup=back_menu_keyboard)

@create_vcc_router.message(CreateVccState.date)
async def get_date(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение запрос даты проведения, запрос времени мероприятия """
    try:
        update_data = parse_datetime(message.text)
    except Exception:
        await message.answer("❌ Вы ввели неверную дату\n\n⚙️ Пример: 28 11 2024 10 10",
        reply_markup=back_menu_keyboard)
        return

    await state.update_data(date=update_data)
    await state.set_state(CreateVccState.duration)
    await message.answer("⌛ Введите продолжительность ВКС в минутах:",
        reply_markup=back_menu_keyboard)


@create_vcc_router.message(CreateVccState.duration)
async def get_duration(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение времени мероприятия, запрос максимального количества """
    try:
        data = int(message.text)
    except ValueError:
        await message.answer("❌ Вы ввели не число!")
        return
    await state.update_data(duration=data)
    await state.set_state(CreateVccState.participants_count_vks)
    await message.answer("🙍 Введите максимальное количество людей в ВКС:",
        reply_markup=back_menu_keyboard)


@create_vcc_router.message(CreateVccState.participants_count_vks)
async def get_participants_count(
        message: Message, 
        state: FSMContext
    ):
    """ сохранение максимального количества, запрос backend """
    try:
        data = int(message.text)
    except ValueError:
        await message.answer("❌ Вы ввели не число!")
        return
    await state.update_data(participants_count=data)
    await state.set_state(CreateVccState.backend)
    await message.answer(
        "⚙️ Выберите тип ВКС:", 
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
        text = "📍 Включать ли микрофон обязательно?",
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
        text = "📍 Включать ли видео обязательно?",
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
        text = "📍 Включать ли ожидание ВКС?",
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
        text = "📍 Включать ли видео запись?",
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
    await callback.message.edit_text(
        "✉️ Введите email пользователей для добавления в ВКС", 
        reply_markup=stop_add_users
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
        text = "📎 Введите ссылку:",
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
        "✉️ Введите email пользователей для добавления в ВКС", 
        reply_markup=stop_add_users
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
        text = "📍 Включать ли видео запись?",
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
    await callback.message.edit_text(
        "✉️ Введите email пользователей для добавления в ВКС", 
        reply_markup=stop_add_users
    )
    



@create_vcc_router.message(CreateVccState.participants)
async def get_participants(
        message: Message, 
        state: FSMContext,
        api_client: AsyncAPIClient,
        token: str
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
        await message.answer("❌ Этот пользователь уже добавлен", reply_markup=stop_add_users)
        return
    data["participants"].append({"id": user_data["data"]["data"][0]["id"]})
    await message.answer("✅ Добавлен", reply_markup=stop_add_users)


@create_vcc_router.callback_query(
        CreateVccState.participants, 
        StopAddUser.filter()
)
async def cancel_participants(
        callback: CallbackQuery, 
        state: FSMContext,
    ):
    await state.set_state(CreateVccState.set_room)
    await callback.message.edit_text(
        text = "🔒 Хотите ли вы указать помещение ВКС?",
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
    if state_data["backend"] == "cisco":
        result = CREATION_VKS_CISCO.format(
            name=data['name_vks'], participantsCount=data['participants_count_vks'],
            startedAt=data['date_vks'], duration=data['duration_vks'],
            backend=data['backend'], 
            isMicrophoneOn='Да' if bool(data['settings']['isMicrophoneOn']) else 'Нет',
            isVideoOn='Да' if bool(data['settings']['isVideoOn']) else 'Нет',
            isWaitingRoomEnabled='Да' if bool(data['settings']['isWaitingRoomEnabled']) else 'Нет',
            needVideoRecording='Да' if bool(data['settings']['needVideoRecording']) else 'Нет'
        )
    elif state_data["backend"] == "external":
        result = CREATION_VKS_EXTERNAL.format(
            name=data['name_vks'], participantsCount=data['participants_count_vks'],
            startedAt=data['date_vks'], duration=data['duration_vks'],
            backend=data['backend'], 
            externalUrl=data['settings']['externalUrl']
        )
    if state_data["backend"] == "vinteo":
        result = CREATION_VKS_VINTEO.format(
            name=data['name_vks'], participantsCount=data['participants_count_vks'],
            startedAt=data['date_vks'], duration=data['duration_vks'],
            backend=data['backend'], 
            needVideoRecording='Да' if bool(data['settings']['needVideoRecording']) else 'Нет'
        )
    await callback.message.edit_text(
        text=result,
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
    ):
    await state.set_state(CreateVccState.building)
    data = await api_client.get_buildings(token)
    await callback.message.edit_text(
        "🔒 Выберите здание, где будет ВКС.", 
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
    ):
    await state.set_state(CreateVccState.room)
    data = await api_client.get_rooms(token, callback_data.id)
    await callback.message.edit_text(
        "🔒 Выберите комнату для ВКС.", 
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
    if state_data["backend"] == "cisco":
        result = CREATION_VKS_CISCO.format(
            name=data['name_vks'], participantsCount=data['participants_count_vks'],
            startedAt=data['date_vks'], duration=data['duration_vks'],
            backend=data['backend'], 
            isMicrophoneOn='Да' if bool(data['settings']['isMicrophoneOn']) else 'Нет',
            isVideoOn='Да' if bool(data['settings']['isVideoOn']) else 'Нет',
            isWaitingRoomEnabled='Да' if bool(data['settings']['isWaitingRoomEnabled']) else 'Нет',
            needVideoRecording='Да' if bool(data['settings']['needVideoRecording']) else 'Нет'
        )
    elif state_data["backend"] == "external":
        result = CREATION_VKS_EXTERNAL.format(
            name=data['name_vks'], participantsCount=data['participants_count_vks'],
            startedAt=data['date_vks'], duration=data['duration_vks'],
            backend=data['backend'], 
            externalUrl=data['settings']['externalUrl']
        )
    if state_data["backend"] == "vinteo":
        result = CREATION_VKS_VINTEO.format(
            name=data['name_vks'], participantsCount=data['participants_count_vks'],
            startedAt=data['date_vks'], duration=data['duration_vks'],
            backend=data['backend'], 
            needVideoRecording='Да' if bool(data['settings']['needVideoRecording']) else 'Нет'
        )
    await callback.message.edit_text(
        text=result,
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
    data = await api_client.create_meeting(
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
        await callback.message.edit_text(
            "❌ Произошла ошибка. Попробуйте ещё раз.\n" + "Детали: " + str(data["data"]['detail']),
            reply_markup=back_menu_keyboard
        )
    else:
        await callback.message.edit_text(
            END_CREATION_VKS.format(permalink=data["data"]['permalink'],
                participants=[participant['email'] for participant in data["data"]['participants']]),
            reply_markup=back_menu_keyboard
            )