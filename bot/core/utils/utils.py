import logging
import re
from typing import Literal

from aiogram import html
from aiogram.types import User


def is_valid_email(email: str) -> bool:
    email_pattern = r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$"
    return bool(re.match(email_pattern, email))