from aiogram import Router

from bot.handlers.Client.start.private import start as private_start


client_router = Router()

client_router.include_routers(
    private_start.router
)