# main.py
import asyncio
from users import get_users_jwt_handler

# Асинхронная функция для инициализации клиента и выполнения запроса
async def main():
    print(get_users_jwt_handler(1241121232))

# Запуск основной асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
