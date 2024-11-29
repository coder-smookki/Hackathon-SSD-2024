import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats

from bot.core.setting import Settings
from bot.core.utils.enums import SlashCommands
from bot.handlers import include_routers


async def on_startup(bot: Bot) -> None:
    user = await bot.me()
    logging.info(
        "Start polling for bot @%s id=%d - %r",
        user.username,
        user.id,
        user.full_name,
    )


async def on_shutdown(bot: Bot) -> None:

    user = await bot.me()
    logging.info(
        "Stop polling for bot @%s id=%d - %r",
        user.username,
        user.id,
        user.full_name,
    )


async def set_commands(bot: "Bot") -> None:
    commands: dict[str, str] = {
        SlashCommands.START: "Старт",
        SlashCommands.HELP: "Помощь",
    }
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in commands.items()
        ],
        scope=BotCommandScopeAllGroupChats(),
    )


def make_disp(settings: Settings) -> "Dispatcher":
    dp = Dispatcher(
        storage=MemoryStorage(),
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
        name="__main__",
        settings=settings,
    )
    include_routers(dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    return dp


def make_bot(bot_token: str) -> "Bot":
    """Create Bot"""
    bot = Bot(token=bot_token)
    return bot
