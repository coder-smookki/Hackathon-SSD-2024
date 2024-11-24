from typing import TYPE_CHECKING

from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from bot.middlewares.request.retry import RetryRequestMiddleware
from bot.middlewares.outer.save_users_id import SaveUsersIdMiddleware


if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher


__all__ = ("setup_global_middlewares",)


def setup_global_middlewares(
    bot: "Bot",
    dp: "Dispatcher",
    # session_maker: "async_sessionmaker[AsyncSession]"
) -> None:
    bot.session.middleware(RetryRequestMiddleware())
    setup_outer_middlewares(dp)
    # setup_inner_middlewares(dp)


def setup_outer_middlewares(
        dp: "Dispatcher",
) -> None:
    # dp.update.outer_middleware(SaveUsersIdMiddleware())
    # dp.message.outer_middleware(SaveUsersIdMiddleware())
    dp.callback_query.outer_middleware(SaveUsersIdMiddleware())
    dp.message.outer_middleware(SaveUsersIdMiddleware())