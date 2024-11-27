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
        event_chat: Chat | None = data.get("event_chat")
        event_router: Router | None = data.get("event_router")
        state: FSMContext = data["state"]
        state_data = await state.get_data()

        if event_router is not None and \
                event_router.name in self.exceptions_router:
            return await handler(event, data)
        
        print(state_data.keys())
        if state_data.get("confirm_check_data") is not None:
            return await handler(event, data)

        await bot.send_message(event_chat.id, "Неизвестный юзер.\nНажмите /start")