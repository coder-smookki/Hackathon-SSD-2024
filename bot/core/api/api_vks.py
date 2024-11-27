import httpx
from typing import Optional, Any
import aiohttp
import asyncio


async def initialize_api_client():
    base_url = "https://test.vcc.uriit.ru/api/"
    headers = {
        "Content-Type": "application/json"
    }

    # Данные для авторизации
    data = {
        'login': 'Hantaton01',
        'password': 't6vYHnNhBqN1F4(q',
    }

    # Создаем экземпляр клиента
    api_client = AsyncAPIClient(base_url, headers)
    # Выполняем асинхронную аутентификацию и получаем токен
    await api_client.authenticate(login_data=data)
    return api_client



class AsyncAPIClient:
    _instance: Optional["AsyncAPIClient"] = None
    _client: Optional[httpx.AsyncClient] = None
    token: Optional[str] = None

    def __new__(self, base_url: str = None, headers: dict = None):
        # создаем экземпляр только один раз
        if self._instance is None:
            self._instance = super(AsyncAPIClient, self).__new__(self)
            self._instance.base_url = base_url or "https://test.vcc.uriit.ru/api/"
            self._instance.headers = headers if headers else {}
            self._instance._client = httpx.AsyncClient(base_url=self._instance.base_url, headers=self._instance.headers)
        return self._instance

    async def get_token(self, login: str, password: str):
        # Выполним запрос на аутентификацию
        response = await self._make_request(
            'POST',
            'auth/login', 
            data={"login": login, "password": password}
        )
        if response and 'token' in response:
            return response['token']
        else:
            raise Exception("Failed to authenticate")

    # Универсальный метод для создания запросов
    async def _make_request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> Optional[Any]:
        try:
            if method.upper() == 'GET':
                response = await self._client.get(endpoint, params=params, headers=self.headers)
            elif method.upper() == 'POST':
                response = await self._client.post(endpoint, json=data, headers=self.headers)
            elif method.upper() == 'PUT':
                response = await self._client.put(endpoint, json=data, headers=self.headers)
            elif method.upper() == 'DELETE':
                response = await self._client.delete(endpoint, params=params, headers=self.headers)
            else:
                raise ValueError("Unsupported HTTP method")

            # Проверка успешности запроса (status code 200-299)
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as e:
            # Обработка ошибок запроса
            print(f"Error during {method} request to {endpoint}: {e}")
            return None
        except httpx.HTTPStatusError as e:
            print(f"HTTP error during {method} request to {endpoint}: {e}")
            return None
            

    # Получение jwt токена для админа
    async def get_token(self):
        return self.token
    

    # Получение jwt токена для пользователя
    async def auth_login(self, login: str = None, password: str = None, params: dict = None) -> Optional[Any]:
        data = {  
            "login": login,
            "password": password,
        }

        headers = {
            'Content-Type': 'application/json',  # Тип содержимого JSON
        }
                
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/login', json=data, headers=headers) as response:
                if response.status == 200:
                    response_data = await response.json()
                    token = response_data.get('token') 
                    return token
                else:
                    print(f"Ошибка: {response.status}")
    
    
    # Регистрация пользователя
    async def auth_register(self,
                            login: str = None,
                            password: str = None,
                            email: str = None,
                            lastName: str = None,
                            firstName: str = None,
                            middleName: str = None,
                            phone: str = None,
                            birthday: str = None,
                            roleId: int = None,
                            params: dict = None) -> Optional[Any]:
        
        data = {
                "login": login,
                "password": password,
                "email": email,
                "lastName": lastName,
                "firstName": firstName,
                "middleName": middleName,
                "phone": phone,
                "birthday": birthday,
                "roleId": roleId,
                "type": "native"
        }


        headers = {
            'Content-Type': 'application/json',
        }

                        
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/register', json=data, headers=headers) as response:
                if response.status == 200:
                    response_data = await response.json()
                    token = response_data.get('token') 
                    return token
                else:
                    print(f"Ошибка: {response.status}")


    # requests users {
    async def get_users(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'users')

    async def get_users_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'users/{id}')
        
    async def create_user(self,
                            login: str = None,
                            password: str = None,
                            email: str = None,
                            lastName: str = None,
                            firstName: str = None,
                            middleName: str = None,
                            phone: str = None,
                            birthday: str = None,
                            roleId: int = None,
                            params: dict = None, 
                            data: dict = None) -> Optional[Any]:
        data = {
            "login": login,
            "password": password,
            "email": email,
            "lastName": lastName,
            "firstName": firstName,
            "middleName": middleName,
            "phone": phone,
            "birthday": birthday,
            "roleIds": [
                roleId
            ],
            "priority": 3,
            "departmentId": 1,
            "isSendEmail": True
        }

        return await self._make_request('POST', f'users', data=data)
    # }
    
    # requests rooms {
    async def get_rooms(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'catalogs/rooms')

    async def get_rooms_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'catalogs/rooms/{id}')

    # Не должно работать
    async def create_room(self, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'catalogs/rooms', data=data)
    # }
    
    # requests events {
    async def get_events(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'events')

    async def get_events_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'events/{id}')

    # Не должно работать
    async def create_event(self, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'events', data=data)
    # }
    
    # requests meetings {
    async def get_meetings(self, params: dict = None, data: dict = None, toDatetime: str = None, fromDatetime: str = None ) -> Optional[Any]:
        params = {
            'state': 'started',
            'toDatetime': toDatetime,
            'fromDatetime': fromDatetime,
        }
        
        return await self._make_request('GET', 'meetings', data=data, params=params)

    async def get_meetings_by_id(self, id: int, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'meetings/{id}', data=data)

    async def create_meeting(self, params: dict = None,
                            custom_data: dict = None,
                            name_vks: str = None,
                            date_vks: str = None, 
                            duration_vks: int = None, 
                            participants_count_vks: int = None, 
                            organizer: dict = None,
                            participants: list[dict] = None, 
                            room_id: int = None,
                            means_conducting: str = None) -> Optional[Any]:
        
        if custom_data is None:

            data = { 
                    "name": name_vks,
                    "roomId": room_id,
                    "comment": "string",
                    "roomId": room_id,
                    "participantsCount": participants_count_vks,
                    "sendNotificationsAt": date_vks,
                    "startedAt": date_vks,
                    "duration": duration_vks,
                    "ciscoSettings": {
                    "isMicrophoneOn": True,
                    "isVideoOn": True,
                    "isWaitingRoomEnabled": True,
                    "needVideoRecording": False
                    },
                    "vinteoSettings": {
                        "needVideoRecording": False
                    },
                    "participants": participants,
                    "recurrenceUpdateType": "only",
                    "isVirtual": False,
                    "state": "booked",
                    "backend": means_conducting,
                    "createdUser": {
                        "id": 546,
                        "lastName": "Хантатонов",
                        "firstName": "Хантатон",
                        "middleName": "",
                        "roleIds": [3],
                        "departmentId": 2,
                        "email": "hantaton03.h@mail.ru"
                    },
                    "organizedBy": {
                        "id": organizer['id']
                    }
            }

        return await self._make_request('POST', 'meetings', data=data)
    # }
    
    
    #Закрыть клиент при завершении работы.
    async def close(self):
        await self._client.aclose()
