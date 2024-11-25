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


    api_client = AsyncAPIClient(base_url, headers, login_data=data)
    return api_client


class AsyncAPIClient:
    _instance: Optional["AsyncAPIClient"] = None
    _client: Optional[httpx.AsyncClient] = None
    token: str = None

    def __new__(self, base_url: str = None, headers: dict = None, login_data: str = None):

        responce = self._make_request(method='GET', endpoint='auth/login', data=login_data)
        self.token = responce.json().get('token')
        self.headers['Authorization'] = f'Bearer {self.token}'  # Добавляем токен в заголовок

        if self._instance is None:
            self._instance = super(AsyncAPIClient, self).__new__(self)
            
            self._instance.base_url = base_url or "https://test.vcc.uriit.ru/api/"
            self._instance.headers = headers if headers else {}
            self._instance._client = httpx.AsyncClient(base_url=self._instance.base_url, headers=self._instance.headers)
        return self._instance

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

    async def get_users(self, endpoint: str, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'users', headers=self.headers)
    
    async def get_users_by_id(self, id: int, endpoint: str, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'users{id}', headers=self.headers)
        
    async def create_user(self, endpoint: str, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', f'users{id}', data=data, headers=self.headers)
    
    async def get_rooms(self, endpoint: str, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'catalogs/rooms', headers=self.headers)

    async def get_rooms_by_id(self, id: int, endpoint: str, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'catalogs/rooms/{id}', headers=self.headers)

    async def create_room(self, endpoint: str, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'catalogs/rooms', data=data, headers=self.headers)
    
    async def get_events(self, endpoint: str, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'events', headers=self.headers)

    async def get_events_by_id(self, id: int, endpoint: str, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'events/{id}', headers=self.headers)

    async def create_event(self, endpoint: str, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'events', data=data, headers=self.headers)
    
    #Закрыть клиент при завершении работы.
    async def close(self):
        await self._client.aclose()
