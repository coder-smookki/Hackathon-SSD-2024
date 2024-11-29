from aiogram import Router

from bot.handlers.get_vcc.start import start_router
from bot.handlers.get_vcc.filters.filters import filter_router
from bot.handlers.get_vcc.pagination.pagination import pagination_router



""" 
Главный роутер
"""
get_vcc_router = Router(name=__name__)

get_vcc_router.include_routers(
    start_router, filter_router, pagination_router
)