# main.py
import asyncio
from api_connection import initialize_api_client

# Асинхронная функция для инициализации клиента и выполнения запроса
async def main():
    client = await initialize_api_client()  # Используем await, чтобы дождаться результата
    users = await client.get_users_by_id(1)  # Получаем пользователей (тоже асинхронный запрос)
    print(users)
    events = await client.get_events()  # Получаем пользователей (тоже асинхронный запрос)
    print(events)
    users = await client.get_users_by_id(1)  # Получаем пользователей (тоже асинхронный запрос)
    print(users)
    print(await client.get_token())

# Запуск основной асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())