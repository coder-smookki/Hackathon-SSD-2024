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

    async def get_users(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'users')

    async def get_users_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'users/{id}')
        
    async def create_user(self, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', f'users', data=data)
    
    async def get_rooms(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'catalogs/rooms')

    async def get_rooms_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'catalogs/rooms/{id}')

    async def create_room(self, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'catalogs/rooms', data=data)
    
    async def get_events(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'events')

    async def get_events_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'events/{id}')

    async def create_event(self, endpoint: str, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'events', data=data)
    
    async def get_meetings(self, endpoint: str, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'meetings?force=true')

    async def get_meetings_by_id(self, id: int, endpoint: str, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'meetings/{id}')

    async def create_meeting(self, endpoint: str, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'meetings?force=true', data=data)
    
    
    #Закрыть клиент при завершении работы.
    async def close(self):
        await self._client.aclose()
