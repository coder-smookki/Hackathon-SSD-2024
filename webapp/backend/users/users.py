from typing import Union

from fastapi import APIRouter, HTTPException

from database.repositories.user_repo import UserAlchemyRepo
# from web_panel.config import db_url
# from web_panel.initialize import database_connection_init

from sqlalchemy import select
import asyncio

from database.models import UserModel
from database.session import database_init
from database.settings import get_settings


users_router = APIRouter()


#@users_router.get("/api/users_jwt", response_model=Union[dict, list])
async def get_users_jwt_handler(tg_id) -> Union[dict, list]:
    settings = get_settings()
    session_maker = await database_init(settings.db)

    async with session_maker() as session:

        result = await session.execute(select(UserModel).filter(UserModel.tg_id == tg_id))
        user = result.scalar_one_or_none()
        
        session.close()

    if user is None:
            raise HTTPException(status_code=404, detail="User not found")

    return {"status": "200 ok", "users": user}


# Асинхронная функция для инициализации клиента и выполнения запроса
async def main():
    print(get_users_jwt_handler(1241121232))

# Запуск основной асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
