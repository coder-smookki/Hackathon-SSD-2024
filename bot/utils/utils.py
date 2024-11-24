from aiogram.types import User


def extract_username(from_user: "User") -> str | None:
    return from_user.username or from_user.first_name or from_user.last_name