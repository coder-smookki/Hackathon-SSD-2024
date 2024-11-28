from aiogram import Dispatcher

from bot.handlers.start import start
from bot.handlers.profile.profile import router
from bot.handlers.authorization.auth_users import router_auth
from bot.handlers.main_menu.main_menu import main_menu_router
from bot.handlers.logout.logout import logout_router
from bot.handlers.view_vks.view_vks import view_vks_router
from bot.handlers.back_menu.back_menu import back_menu_router



def include_routers(dp: "Dispatcher") -> None:
    dp.include_routers(
        start.router,
        router_auth,
        router,
        main_menu_router,
        logout_router,
        view_vks_router,
        back_menu_router
    )