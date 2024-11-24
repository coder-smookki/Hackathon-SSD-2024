from abc import ABC

from core.models.user import User
from core.repositories.abc_meta import RepoMeta


class UserRepo(RepoMeta[User, User, int], ABC):
    pass