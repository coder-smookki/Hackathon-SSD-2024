import httpx
from typing import Optional, Any


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
    api_client = AsyncAPIClient(base_url, headers, login_data=data)
    # Выполняем асинхронную аутентификацию и получаем токен
    await api_client.authenticate(login_data=data)
    return api_client


class AsyncAPIClient:
    _instance: Optional["AsyncAPIClient"] = None
    _client: Optional[httpx.AsyncClient] = None
    token: Optional[str] = None

    def __new__(self, base_url: str = None, headers: dict = None, login_data: dict = None):
        # создаем экземпляр только один раз
        if self._instance is None:
            self._instance = super(AsyncAPIClient, self).__new__(self)
            self._instance.base_url = base_url or "https://test.vcc.uriit.ru/api/"
            self._instance.headers = headers if headers else {}
            self._instance._client = httpx.AsyncClient(base_url=self._instance.base_url, headers=self._instance.headers)
        return self._instance

    async def authenticate(self, login_data: dict):
        # Выполним запрос на аутентификацию
        response = await self._make_request('POST', 'auth/login', data=login_data)
        if response and 'token' in response:
            self.token = response['token']
            self.headers['Authorization'] = f'Bearer {self.token}'  # Добавляем токен в заголовок
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
        
    async def get_token(self):
        return self.token

    # requests users {
    async def get_users(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'users')

    async def get_users_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'users/{id}')
        
    async def create_user(self, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', f'users', data=data)
    # requests users }
    
    # requests rooms {
    async def get_rooms(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'catalogs/rooms')

    async def get_rooms_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'catalogs/rooms/{id}')

    async def create_room(self, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'catalogs/rooms', data=data)
    # requests rooms }
    
    # requests events {
    async def get_events(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'events')

    async def get_events_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'events/{id}')

    async def create_event(self, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'events', data=data)
    # requests events }
    
    # requests meetings {
    async def get_meetings(self, params: dict = None, data: dict = None, toDatetime: str = None, fromDatetime: str = None ) -> Optional[Any]:
        params = {
            'state': 'started',
            'toDatetime': toDatetime,
            'fromDatetime': fromDatetime,
        }
        
        return await self._make_request('GET', 'meetings', data=data, params=params)
        #return await self._make_request('GET', 'meetings?state=started&toDatetime=2024-11-26T23%3A00%3A00.000000&fromDatetime=2024-11-25T00%3A00%3A00.000000', data=data)


    async def get_meetings_by_id(self, id: int, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'meetings/{id}', data=data)

    async def create_meeting(self, params: dict = None,
                            
                            name_vks: str = None,
                            date_vks: str = None, 
                            duration_vks: int = None, 
                            participants_count_vks: int = None, ) -> Optional[Any]:
        data ={
            "name": name_vks,
            "comment": "string",
            "participantsCount": participants_count_vks,
            "sendNotificationsAt": "2024-11-25T17:32:00.000000",
            "startedAt": date_vks,
            "duration": duration_vks,
            "ciscoSettings": {
            "isMicrophoneOn": true,
            "isVideoOn": true,
            "isWaitingRoomEnabled": true,
            "needVideoRecording": false
        },
        "vinteoSettings": {
            "needVideoRecording": false
        },
            "participants": [
                {
                    "id": 544,
                    "email": "hantaton10.h@mail.ru",
                    "lastName": null,
                    "firstName": null,
                    "middleName": null,
                    "isApproved": null
                }
            ],
            "recurrenceUpdateType": "only",
            "isVirtual": false,
            "state": "booked",
            "backend": "cisco",
            "organizedBy": {
            "id": 544
        }
        }

        return await self._make_request('POST', 'meetings', data=data)
    # requests meetings }
    
    
    #Закрыть клиент при завершении работы.
    async def close(self):
        await self._client.aclose()
