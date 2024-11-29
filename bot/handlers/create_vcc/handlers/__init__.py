from bot.handlers.create_vcc.handlers.base_data import base_data_vcc_router
from bot.handlers.create_vcc.handlers.check_data import check_data_vcc_router
from bot.handlers.create_vcc.handlers.cisco import cisco_vcc_router
from bot.handlers.create_vcc.handlers.external import external_vcc_router
from bot.handlers.create_vcc.handlers.participants import participants_vcc_router
from bot.handlers.create_vcc.handlers.room import room_vcc_router
from bot.handlers.create_vcc.handlers.vinteo import vinteo_vcc_router

routers = (
    base_data_vcc_router,
    check_data_vcc_router,
    cisco_vcc_router,
    external_vcc_router,
    vinteo_vcc_router,
    room_vcc_router,
    participants_vcc_router,
)
