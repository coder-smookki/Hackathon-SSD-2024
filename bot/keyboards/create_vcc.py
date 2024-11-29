from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.create_vcc import (
    ChooseBackendVcc,
    ChooseBuilding,
    ChooseRoom,
    StopAddUser,
)

choose_backend_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="cisco",
                callback_data=ChooseBackendVcc(name="cisco").pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="external",
                callback_data=ChooseBackendVcc(name="external").pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="vinteo",
                callback_data=ChooseBackendVcc(name="vinteo").pack(),
            ),
        ],
    ],
)

stop_add_users = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Прекратить добавлять людей",
                callback_data=StopAddUser().pack(),
            ),
        ],
    ],
)


def create_choose_building_keyboard(buildings: list[dict]):
    mass = []
    for building in buildings:
        mass.append(
            [
                InlineKeyboardButton(
                    text=building["name"],
                    callback_data=ChooseBuilding(id=building["id"]).pack(),
                ),
            ],
        )
    return InlineKeyboardMarkup(inline_keyboard=mass)


def create_choose_room_keyboard(rooms: list[dict]):
    mass = []
    for room in rooms:
        mass.append(
            [
                InlineKeyboardButton(
                    text=room["name"],
                    callback_data=ChooseRoom(id=room["id"]).pack(),
                ),
            ],
        )
    return InlineKeyboardMarkup(inline_keyboard=mass)
