from aiogram.filters import BaseFilter
from aiogram.types import Message


class EmailExistsFilter(BaseFilter):
    async def __call__(self, message: Message, user_info: dict | None) -> bool:
        """
        Проверяем, что email в user_info не равен None и не равен "Не указано".
        """
        if user_info is None:
            return False

        email = user_info.get("email")
        return email is not None


class EmailNotExistsFilter(BaseFilter):
    async def __call__(self, message: Message, user_info: dict | None) -> bool:
        """
        Проверяем, что email в user_info равен None или "Не указано".
        """
        if user_info is None:
            return True

        email = user_info.get("email")
        return email is None
