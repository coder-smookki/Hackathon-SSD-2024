import os
from functools import lru_cache

from pydantic import BaseModel


class DBSettings(BaseModel):
    """Настройки подключения к базе данных."""

    host: str
    host_port: int
    db: str
    user: str
    password: str



class BotSettings(BaseModel):
    """Настройки телеграм-бота."""

    token: str


class Settings(BaseModel):
    """Сборник настроек :)."""

    db: DBSettings
    bot: BotSettings


@lru_cache
def get_settings() -> Settings:
    """
    Создание настроек из переменных среды.

    :return: Настройки.
    """
    db = DBSettings(
        host=os.environ["DB_HOST"],
        host_port=int(os.environ["DB_PORT"]),
        db=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    bot = BotSettings(
        token=os.environ["BOT_TOKEN"],
    )



    return Settings(db=db, bot=bot)