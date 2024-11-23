from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats


from bot.handlers import include_routers
from bot.core.enums import SlashCommands


async def set_commands(bot: "Bot") -> None:
    commands: dict[str, str] ={
        SlashCommands.START: "Старт",
        SlashCommands.HELP: "Помощь"
    }
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in commands.items()
        ], scope=BotCommandScopeAllGroupChats(),
    )


def make_disp() -> "Dispatcher":
    dp = Dispatcher(
        storage=MemoryStorage(),
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
        name="__main__"
    )
    include_routers(dp)
    return dp


def make_bot(bot_token: str) -> "Bot":
    """Create Bot"""
    bot = Bot(token=bot_token)
    return bot

