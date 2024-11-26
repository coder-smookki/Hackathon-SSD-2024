# main.py
import asyncio
from api_vks import initialize_api_client

# Асинхронная функция для инициализации клиента и выполнения запроса
async def main():
    client = await initialize_api_client()  # Используем await, чтобы дождаться результата
    print('\n\n')
    print(await client.get_meetings_by_id(1121))
    # print('\n\n')
    # print(await client.create_meeting(name_vks='gogogg', date_vks="2024-11-25T17:32:00.000000", 
    #                         duration_vks=52, 
    #                         participants_count_vks=2))
    
    # print(await client.get_meetings(toDatetime='2024-11-26T23:00:00.000000', fromDatetime='2023-11-25T00:00:00.000000'))
    

# Запуск основной асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
