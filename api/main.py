# main.py
import asyncio
from api_vks import initialize_api_client, AsyncAPIClient
import requests


# Асинхронная функция для инициализации клиента и выполнения запроса
async def main():
    client = await initialize_api_client()  # Используем await, чтобы дождаться результата

    # Создание ВКС
    organizer = {
                            "id": 544,
                            "email": "hantaton10.h@mail.ru",
                            "lastName": None,
                            "firstName": None,
                            "middleName": None,
                            "isApproved": None
                        }
    
    participants = [
        {
            "id": 1,
            "email": "yakimchukav@uriit.ru",
            "lastName": None,
            "firstName": None,
            "middleName": None,
            "isApproved": None
        },
        {
            "id": 569,
            "email": "afafda.h@mail.ru",
            "lastName": None,
            "firstName": None,
            "middleName": None,
            "isApproved": None
        }
    ]

    participants.insert(0, organizer)
    print(participants)

    print('\n\n')
    print(await client.create_meeting(name_vks='asdfdasfkekeke', date_vks='2024-11-25T17:33:00.000000',
                                       duration_vks=52, participants_count_vks=3, organizer=organizer, participants=participants,
                                       room_id=1, means_conducting='cisco'))
    print('\n\n')

    # Регистрация пользователя и заход с его данными
    print(await client.auth_register(login='bobi', password='string12343', email='bobi@example.com',
                                      lastName='string12343', firstName='string12343', middleName='string12343',
                                        phone='string12343', birthday='2024-11-26', roleId=5))
    print('\n\n')
    print(await client.auth_login(login='bobi', password='string12343'))
    print(await client.auth_login(login='string12343', password='string12343'))
    print(await client.get_users())

    # Выбор ВКС в периоде с fromDatetime для toDatetime
    print('\n\n')
    print(await client.get_meetings(toDatetime='2024-11-26T23:00:00.000000', fromDatetime='2023-11-25T00:00:00.000000'))
    

# Запуск основной асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
