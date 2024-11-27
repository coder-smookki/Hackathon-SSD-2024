from typing import Callable, Dict, Any
from datetime import datetime

from aiogram import BaseMiddleware, Bot, Router
from aiogram.types import TelegramObject, Chat
from aiogram.fsm.context import FSMContext

from bot.core.api.api_vks import AsyncAPIClient


class AuthMiddleware(BaseMiddleware):
    """
    Middleware для авторизации, выполняется только при состоянии confirm.
    """
    def __init__(self, exceptions_router: list[str]):
        self.exceptions_router = exceptions_router
        super().__init__()


    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Выполнение middleware при достижении состояния ExtractData.confirm.
        """
        # TODO 
        bot: Bot = data["bot"]
        user: dict | None = data.get("user_info")
        event_chat: Chat | None = data.get("event_chat")
        event_router: Router | None = data.get("event_router")
        state: FSMContext = data["state"]
        state_data = await state.get_data()

        # если процесс авторизации еще идет
        if event_router is not None and \
                event_router.name in self.exceptions_router:
            return await handler(event, data)

        # если хуй без токена
        if state_data.get("token") is None:
            await bot.send_message(event_chat.id, "Нажмите /start")
            return
        
        # если токен еще не истек
        if state_data["expired_time"] > datetime.now():
            data["token"] = state_data["token"]
            return await handler(event, data)
        
        if state_data.get("confirm_save_data"):
            token = await AsyncAPIClient().get_token(
                state_data["login"], state_data["password"]
            )
            await state.update_data("token", token)
            data["token"] = token
            return await handler(event, data)
        else:
            await state.clear()
            # нужен откат до авторизации
            await bot.send_message(event_chat.id, "Нажмите /start")