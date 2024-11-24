from aiogram import Router

from bot.handlers.Client.start.private import start as private_start
from bot.handlers.Client.authorization.auth_users import router_auth


client_router = Router()

client_router.include_routers(
    private_start.router,
    router_auth
)