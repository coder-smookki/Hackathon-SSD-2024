from database.schemas.base import BaseDTO


class UserDTO(BaseDTO):
    tg_id: int
    login: str | None
    email: str | None
    password: str | None
    jwt_token: str | None
