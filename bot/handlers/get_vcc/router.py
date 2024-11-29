from aiogram import Router

from bot.handlers.get_vcc.filters import routers
from bot.handlers.get_vcc.pagination.pagination import pagination_router
from bot.handlers.get_vcc.start import start_router

get_vcc_router = Router(name=__name__)

get_vcc_router.include_routers(start_router, pagination_router, *routers)
