from aiogram.types import User, CallbackQuery, Message


def extract_username(from_user: User) -> str | None:
    return from_user.username or from_user.first_name or from_user.last_name

def extract_chat_id(event: CallbackQuery | Message) -> int | None:
    if isinstance(event, CallbackQuery):
        event = event.message
    return event.chat.id