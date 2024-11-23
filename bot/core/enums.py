from enum import Enum


class Commands(str, Enum):
    START = "Client"
    HELP = "help"
    PROFILE = "profile"