from typing import Callable, Dict, Any
from datetime import datetime

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Chat
from aiogram.fsm.context import FSMContext

from bot.core.api.api_vks import AsyncAPIClient
from bot.core.utils.jwt import parse_token, get_expired_time_token
from database.models import UserModel
from database.repositories import UserAlchemyRepo


class JWTMiddleware(BaseMiddleware):
    """
    Middleware проверяет jwt токен, при необходимости обновляет его
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data["bot"]
        event_chat: Chat | None = data.get("event_chat")
        user: UserModel = data.get("user")
        user_repo: UserAlchemyRepo = data["user_repo"]
        api_client: AsyncAPIClient = data.get("api_client")

        state: FSMContext = data["state"]
        state_data = await state.get_data()

        if user is None:
            data["token"] = None
            return await handler(event, data)

        # если токен еще не истек
        if datetime.now() < user.token_expired_at:
            data["token"] = user.token
            return await handler(event, data)
        
        # Обновление токена
        if datetime.now() < user.refresh_token_expired_at:
            new_data = await api_client.update_token(user.refresh_token) # TODO rename
            token_data = parse_token(new_data["token"])
            user.token_expired_at = get_expired_time_token(new_data["token"])
            user.refresh_token = token_data["refresh_token"]
            user.refresh_token_expired_at = get_expired_time_token(user.refresh_token)

            if new_data["user"]["birthday"] is not None:
                user_birthday = datetime.strptime(new_data["user"]["birthday"], "%Y-%m-%d").date()
            else: 
                user_birthday = None

            user.first_name=new_data["user"]["firstName"]
            user.last_name=new_data["user"]["lastName"]
            user.midle_name=new_data["user"]["middleName"]
            user.birthday=user_birthday
            user.phone=new_data["user"]["phone"]

            user = await user_repo.update(user)

            data["token"] = user.token
            return await handler(event, data)

        # заставить юзера прислать пароль
