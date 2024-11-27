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
    MENU = "menu"
    HELP = "help"
    PROFILE = "profile"
    AUTHORIZATIONS = "authorization"


class TextCommands(str, Enum):
    HELP = 'Помощь'
    PROFILE = 'Профиль'
    MAIN_MENU = 'Главное меню'
    VIEW_VKS = 'Просмотр ВКС'
    LOGOUT = 'Выйти из аккаунта'
    AUTHORIZATIONS = "Авторизация"


class Operation(str, Enum):
    '''Для Callbacks'''

    PROFILE = "profile"
    MENU = "menu"
    VIEW_VKS = "view_vks"
    AUTHORIZATIONS = "authorization"
    CANCEL = "cancel"
    CONFIRM = "confirm"
    START = "start"
    LOGOUT = "logout"


class BotMenu(StrEnum):
    START = "start"
    PROFILE = "profile"
    AUTHORIZATIONS = "authorization"