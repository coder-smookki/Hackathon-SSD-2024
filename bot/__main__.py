import asyncio
import contextlib

from dotenv import load_dotenv
import os

from middlewares import setup_global_middlewares
from core.factories import make_bot, make_disp


async def main() -> None:
    load_dotenv()

    dp = make_disp()
    bot = make_bot(bot_token=os.getenv("BOT_TOKEN"))

    setup_global_middlewares(bot, dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())