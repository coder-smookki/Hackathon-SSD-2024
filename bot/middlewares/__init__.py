from typing import TYPE_CHECKING

from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from bot.middlewares.request.retry import RetryRequestMiddleware
from bot.middlewares.inner.check_auth import AuthMiddleware
from bot.middlewares.outer.database import DatabaseMiddleware



if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher


__all__ = ("setup_global_middlewares",)


def setup_global_middlewares(
    bot: "Bot",
    dp: "Dispatcher",
    session_maker,
) -> None:
    bot.session.middleware(RetryRequestMiddleware())

    dp.message.middleware(AuthMiddleware([
        "bot.handlers.authorization.auth_users",
        "bot.handlers.start.start",
    ]))
    dp.callback_query.middleware(AuthMiddleware([
        "bot.handlers.authorization.auth_users",
        "bot.handlers.start.start", 
    ]))
    
    setup_outer_middlewares(dp, session_maker)
    # setup_inner_middlewares(dp)


def setup_outer_middlewares(
        dp: "Dispatcher",
        session_maker
) -> None:
    dp.update.outer_middleware(DatabaseMiddleware(session_maker))