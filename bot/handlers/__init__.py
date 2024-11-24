from aiogram import Dispatcher
from handlers.Client import client_router


def include_routers(dp: "Dispatcher") -> None:
    dp.include_routers(
        client_router
    )