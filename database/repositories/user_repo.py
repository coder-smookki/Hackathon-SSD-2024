from typing import Optional

from sqlalchemy import delete, select

from core.models import User
from core.repositories import UserRepo
from database.models import UserModel
from database.repositories.base import BaseAlchemyRepo


class UserAlchemyRepo(UserRepo, BaseAlchemyRepo):
    async def create(self, instance: User) -> User:
        """
        Создание пользователя в базе данных.

        :param instance: Экземпляр User (данные пользователя).
        :return: Экземпляр User (с обновленными данными).
        """
        user = UserModel(**instance.model_dump())  # Преобразуем данные из User в модель базы данных
        self.session.add(user)
        await self.session.commit()

        model = await self.get(instance.id)  # Получаем модель из базы данных по ID
        return model  # Возвращаем модель User, без обертки UserExtended

    async def delete(self, tg_id: int) -> None:
        """
        Удаление пользователя по ID.

        :param tg_id:  ID пользователя, которого нужно удалить.
        """
        query = delete(UserModel).where(UserModel.tg_id == tg_id)
        await self.session.execute(query)
        await self.session.commit()

    async def get(self, tg_id: int) -> Optional[UserModel]:
        """
        Получение пользователя по ID.

        :param tg_id: ID пользователя.
        :return: Экземпляр модели UserModel или None, если не найден.
        """
        query = select(UserModel).where(UserModel.tg_id == tg_id)
        model = await self.session.scalar(query)  # Получаем один результат
        return model  # Возвращаем саму модель UserModel или None, если пользователь не найден

    async def update(self, tg_id: int, instance: User) -> UserModel:
        """
        Обновление данных пользователя.

        :param tg_id: ID пользователя.
        :param instance: Экземпляр User с обновленными данными.
        :return: Обновленная модель UserModel.
        """
        instance.id = tg_id  # Устанавливаем ID на объекте
        model = UserModel(**instance.model_dump())  # Преобразуем в модель базы данных
        await self.session.merge(model)  # Мержим изменения с базой данных
        await self.session.commit()

        updated_model = await self.get(tg_id)  # Получаем обновленную модель из базы данных
        return updated_model  # Возвращаем обновленную модель UserModel