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
    START = "Client"
    HELP = "help"
    PROFILE = "profile"


class TextCommands(str, Enum):
    HELP = 'Помощь'
    PROFILE = 'Профиль'


class Operation(str, Enum):
    '''Для Callbacks'''

    PROFILE = "profile"
    AUTHORIZATIONS = "authorization"