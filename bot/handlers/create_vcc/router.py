from aiogram import Router

from bot.handlers.create_vcc.handlers import routers

create_vcc_router = Router(name=__name__)
create_vcc_router.include_routers(*routers)
