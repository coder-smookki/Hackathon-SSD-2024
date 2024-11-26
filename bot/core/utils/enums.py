from enum import Enum


class ValuesEnum(Enum):
    @classmethod
    def values(cls) -> list[str]:
        return [e.value for e in cls]


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str(self.value)
    

class ProfileField(StrEnum, ValuesEnum):
    EMAIL = "email"
    LOGIN = "login"
    PASSWORD = "password"


class SlashCommands(str, Enum):
    START = "start"
    HELP = "help"
    PROFILE = "profile"
    AUTHORIZATIONS = "authorization"


class TextCommands(str, Enum):
    HELP = 'Помощь'
    PROFILE = 'Профиль'
    AUTHORIZATIONS = "Авторизация"


class Operation(str, Enum):
    '''Для Callbacks'''

    PROFILE = "profile"
    AUTHORIZATIONS = "authorization"
    CANCEL = "cancel"
    CONFIRM = "confirm"
    START = "start"


class BotMenu(StrEnum):
    START = "start"
    PROFILE = "profile"
    AUTHORIZATIONS = "authorization"