from aiogram import Router

from handlers.Client.start.private import start as private_start
from handlers.Client.authorization.auth_users import router_auth
from handlers.Client.profile.profile import router as profile_router


client_router = Router()

client_router.include_routers(
    private_start.router,
    router_auth,
    profile_router
)