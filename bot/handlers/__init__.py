from aiogram import Dispatcher

from bot.handlers.start import start
from bot.handlers.profile.profile import router
from bot.handlers.authorization.auth_users import router_auth
from bot.handlers.main_menu.main_menu import main_menu_router



def include_routers(dp: "Dispatcher") -> None:
    dp.include_routers(
        start.router,
        router_auth,
        router,
        main_menu_router
    )