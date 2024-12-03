from typing import TYPE_CHECKING

from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from bot.middlewares.inner.check_auth import AuthMiddleware
from bot.middlewares.outer import (
    DatabaseMiddleware,
    JWTMiddleware,
    LoggingMiddleware,
    ServiceDIMiddleware,
    ThrottlingMiddleware,
    UserContextMiddleware,
)
from bot.middlewares.request.retry import RetryRequestMiddleware

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher


__all__ = ("setup_global_middlewares",)


def setup_global_middlewares(
    bot: "Bot",
    dp: "Dispatcher",
    session_maker,
) -> None:
    bot.session.middleware(RetryRequestMiddleware())

    setup_outer_middlewares(dp, session_maker)
    setup_inner_middlewares(dp)


def setup_inner_middlewares(dp: "Dispatcher") -> None:
    dp.message.middleware(
        AuthMiddleware(
            [
                "bot.handlers.authorization.auth_users",
                "bot.handlers.start.start",
            ],
        ),
    )
    dp.callback_query.middleware(
        AuthMiddleware(
            [
                "bot.handlers.authorization.auth_users",
                "bot.handlers.start.start",
            ],
        ),
    )


def setup_outer_middlewares(dp: "Dispatcher", session_maker) -> None:
    JWTMiddleware
    dp.message.outer_middleware(LoggingMiddleware())
    dp.callback_query.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(DatabaseMiddleware(session_maker))
    dp.update.outer_middleware(ServiceDIMiddleware())
    dp.update.outer_middleware(UserContextMiddleware())
    dp.update.outer_middleware(JWTMiddleware())
    dp.update.outer_middleware(ThrottlingMiddleware())
