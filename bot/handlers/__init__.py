from aiogram import Dispatcher

from bot.handlers.start.start import start_router
from bot.handlers.profile.profile import router
from bot.handlers.authorization.auth_users import auth_router
from bot.handlers.menu.main_menu import main_menu_router
from bot.handlers.create_vcc.create_vcc import create_vcc_router
from bot.handlers.get_vcc.main import get_vcc_router
from bot.handlers.logout.logout import logout_router
from bot.handlers.menu.main_menu import back_menu_router




def include_routers(dp: "Dispatcher") -> None:
    dp.include_routers(
        start_router,
        auth_router,
        router,
        main_menu_router,
        create_vcc_router,
        get_vcc_router,
        back_menu_router,
        logout_router
    )