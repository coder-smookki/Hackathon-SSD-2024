from typing import Union

import os, sys
sys.path.insert(1, os.getcwd())
from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException

from sqlalchemy import select
from database.models import UserModel
from database.session import database_init
from database.settings import get_settings


load_dotenv()

users_router = APIRouter()


@users_router.get("/users_jwt", response_model=Union[dict, str])
async def get_users_jwt_handler(tg_id) -> Union[dict, list]:
    settings = get_settings()
    session_maker = await database_init(settings.db)

    async with session_maker() as session:

        result = await session.execute(select(UserModel).filter(UserModel.tg_id == tg_id))
        user = result.scalar_one_or_none()
        
        await session.close()

    if user is None:
            raise HTTPException(status_code=404, detail="User not found")

    return {"status": "200 ok", "user_jwt": user.jwt_token}
