import os
import sys
from typing import Union

<<<<<<< HEAD
import os, sys
sys.path.insert(1, os.getcwd())
=======
>>>>>>> 161edae91ea397ee91c27637176e92985429beac
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database.models import UserModel
from database.session import database_init
from database.settings import get_settings

load_dotenv()

users_router = APIRouter()


<<<<<<< HEAD
@users_router.get("/api/users_jwt/{tg_id}", response_model=Union[dict, str])
async def get_users_jwt_handler(tg_id) -> Union[dict, list]:
=======
@users_router.get("/users_jwt/{tg_id}", response_model=Union[dict, str])
async def get_users_jwt_handler(tg_id) -> dict | list:
>>>>>>> 3263c7a457beb35da22ab05e0d6c86030d8af645

    if not tg_id.isdigit():
        return {"status": "400 bad request", "messages": []}
    tg_id = int(tg_id)

    settings = get_settings()
    session_maker = await database_init(settings.db)

    async with session_maker() as session:

        result = await session.execute(
            select(UserModel).where(UserModel.tg_id == tg_id),
        )
        print(result)
        user = result.scalar_one_or_none()

        # await session.close()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"status": "200 ok", "user_jwt": user.token}
