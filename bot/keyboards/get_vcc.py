from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.callbacks.get_vcc import (
    FilterVcc, 
    PriorityVcc, 
    DepartmenVcc, 
    StateVcc, 
    PagionationVccData,
    CancelFilterDataVcc
)
from bot.core.api.api_vks import MEETINGS_ON_PAGE



def get_filters_keyboard(
        meetings_count: int, 
        page: int
    ):
    back_button = InlineKeyboardButton(
        text="Назад список;", 
        callback_data=PagionationVccData(value=-1).pack()
    ),
    forward_button = InlineKeyboardButton(
        text="Дальше список;", 
        callback_data=PagionationVccData(value=1).pack()
    ),
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Состояние:", callback_data="None"),
            InlineKeyboardButton(
                text="Забронированные", 
                callback_data=StateVcc(name="booked").pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="Начатые", 
                callback_data=StateVcc(name="started").pack()
            ),
            InlineKeyboardButton(
                text="Законченные", 
                callback_data=StateVcc(name="ended").pack()
            ),
        ],    
        [
            InlineKeyboardButton(
                text="Отмененные", 
                callback_data=StateVcc(name="cancelled").pack()
            ),
            InlineKeyboardButton(
                text="Наименование;", 
                callback_data=FilterVcc(name="name").pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="Приоритет;", 
                callback_data=FilterVcc(name="priority").pack()
            ),
            InlineKeyboardButton(
                text="Депортамент;", 
                callback_data=FilterVcc(name="department").pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="Организатор;", 
                callback_data=FilterVcc(name="user").pack()
            ),
        ],
        [

        ],
        [
            InlineKeyboardButton(
                text="Главное меню;", # TODO
                callback_data=StateVcc(name="menu").pack()
            ),
        ],
    ])
    if page != 1:
        keyboard.inline_keyboard[-2] += back_button
    if page*MEETINGS_ON_PAGE < meetings_count:
        keyboard.inline_keyboard[-2] += forward_button
    return keyboard


cancel_name_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="сбос фильтра",
        callback_data=CancelFilterDataVcc(filter_="filter").pack()
    )]
])
cancel_user_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="сбос фильтра",
        callback_data=CancelFilterDataVcc(filter_="userId").pack()
    )]
])


priority_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text = "1", callback_data=PriorityVcc(value=1).pack()
        ),
        InlineKeyboardButton(
            text = "2", callback_data=PriorityVcc(value=2).pack()
        ),
        InlineKeyboardButton(
            text = "3", callback_data=PriorityVcc(value=3).pack()
        ),
    ],
    [InlineKeyboardButton(
        text="сбос фильтра",
        callback_data=CancelFilterDataVcc(filter_="priority").pack()
    )]
])


def create_choose_department_keyboard(departmens: list[dict]):

    mass = [[InlineKeyboardButton(
        text="сбос фильтра",
        callback_data=CancelFilterDataVcc(filter_="departmentId").pack()
    )]]
    for departmen in departmens:
        mass.append([
            InlineKeyboardButton(
                text=departmen["name"],
                callback_data=DepartmenVcc(id=departmen["id"]).pack()
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=mass)