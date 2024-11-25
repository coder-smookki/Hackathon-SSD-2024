
from sqlalchemy import select

from database.models import UserModel
from session import database_init
from settings import get_settings


# async def main():
#
#     settings = get_settings()
#     session_maker = await database_init(settings.db)
#
#     async with session_maker as session:
#         # Добавление данных
#         new_user = UserModel(tg_id=12412, login='login', email='123mail', password='admin', jwt_token='23j4l234l234jl23')  # Пример модели User
#         session.add(new_user)
#         await session.commit()
#
#         # Чтение данных
#         users = await session.execute(select(UserModel))  # Пример модели User
#         for user in users.scalars().all():
#             print(user.login)
#
#         # Обновление данных
#         user_to_update = await session.get(UserModel, 1)  # Пример id = 1
#         if user_to_update:
#             user_to_update.name = "Updated User"
#             await session.commit()
#
#         # Удаление данных
#         user_to_delete = await session.get(UserModel, 1)
#         if user_to_delete:
#             await session.delete(user_to_delete)
#             await session.commit()
#
#     print('Hello world')
#
#
# if __name__ == "__main__":
#     main()


import asyncio
# ... ваши импорты ...

async def main():
  settings = get_settings()
  session_maker = await database_init(settings.db)

  async with session_maker() as session:
    # Добавление данных
    new_user = UserModel(tg_id=12412, login='login', email='123mail', password='admin', jwt_token='23j4l234l234jl23', events=None)
    session.add(new_user)
    await session.commit()

    # Чтение данных
    users = await session.execute(select(UserModel))
    for user in users.scalars().all():
      print(user.login)

    # Обновление данных (будет ошибка, т.к. нет поля name в модели)
    # user_to_update = await session.get(UserModel, 1)
    # if user_to_update:
    #   user_to_update.name = "Updated User"
    #   await session.commit()

    # Удаление данных (тоже будет ошибка, id=1 может не существовать)
    # user_to_delete = await session.get(UserModel, 1)
    # if user_to_delete:
    #   await session.delete(user_to_delete)
    #   await session.commit()

  print('Hello world')

if __name__ == "__main__":
  asyncio.run(main())
