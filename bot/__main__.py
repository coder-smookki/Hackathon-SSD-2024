import asyncio
import contextlib
import logging
import os
import sys

from dotenv import load_dotenv

sys.path.insert(1, os.getcwd())

from bot.core.factories import make_bot, make_disp
from bot.core.setting import get_settings
from bot.middlewares import setup_global_middlewares
from database.session import database_init


async def main() -> None:
    load_dotenv()

    logging.basicConfig(level=logging.DEBUG)

    settings = get_settings()
    dp = make_disp(settings)
    bot = make_bot(bot_token=os.getenv("BOT_TOKEN"))
    session_maker = await database_init(settings.db)

    setup_global_middlewares(bot, dp, session_maker)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
