from enum import Enum


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