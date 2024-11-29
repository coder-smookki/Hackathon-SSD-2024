import re
from datetime import datetime, timedelta

from aiogram.types import User, CallbackQuery, Message


def is_valid_email(email: str) -> bool:
    email_pattern = r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$"
    return bool(re.match(email_pattern, email))


def parse_datetime(string: str) -> str:
    """Парсит дату в формат подходящий для api

    Args:
        string (str): dd mm yyyy hh mm

    Returns:
        str: 
    """
    return (datetime.strptime(string, "%d %m %Y %H %M")
            - timedelta(hours=5)).isoformat() # смещение относительно utc


def extract_username(from_user: User) -> str | None:
    return from_user.username or from_user.first_name or from_user.last_name

def extract_chat_id(event: CallbackQuery | Message) -> int | None:
    if isinstance(event, CallbackQuery):
        event = event.message
    return event.chat.id