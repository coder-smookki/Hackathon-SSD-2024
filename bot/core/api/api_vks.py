from typing import Optional, Any

import aiohttp
import httpx


MEETINGS_ON_PAGE=6


class AuthorizationException(Exception):
    ...

class UpdateTokensException(Exception):
    ...
    

class AsyncAPIClient:
    _instance: Optional["AsyncAPIClient"] = None
    _client: Optional[httpx.AsyncClient] = None
    #headers: Optional[dict] = None
    token: Optional[str] = None

    def __new__(self, base_url: str = None, headers: dict = None):
        # создаем экземпляр только один раз
        if self._instance is None:
            self._instance = super(AsyncAPIClient, self).__new__(self)
            self.session = aiohttp.ClientSession()
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
            

    # Получение jwt токена для пользователя
    async def auth_login(self, login: str, password: str, params: dict = None) -> dict[str, Any]:
        data = {  
            "login": login,
            "password": password,
        }

        headers = {
            'Content-Type': 'application/json',  # Тип содержимого JSON
        }
                
        async with self.session.post('https://test.vcc.uriit.ru/api/auth/login', json=data, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data # для сохранение в бд нужен не только токен
            else:
                print(f"Ошибка: {response.status}")
                raise AuthorizationException
    
    async def update_token(self, refresh_token: str):
        headers = {
            'Content-Type': 'application/json',  # Тип содержимого JSON
        }
        async with self.session.post(
                'https://test.vcc.uriit.ru/api/auth/refresh-token', 
                json={"token": refresh_token}, 
                headers=headers
            ) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data # для сохранение в бд нужен не только токен
            else:
                print(f"Ошибка: {response.status}")
                raise UpdateTokensException
    
    
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

    async def auth_logout(self, token: str = None, params: dict = None):      
        return await self._make_request('POST', '/auth/logout', data=token) 

    # requests users {
    async def get_users(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'users')

    async def get_users_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'users/{id}')
        
    async def create_user(self, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', f'users', data=data)
    # }
    
    # requests rooms {
    async def get_rooms(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'catalogs/rooms')

    async def get_rooms_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'catalogs/rooms/{id}')

    async def create_room(self, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('POST', 'catalogs/rooms', data=data)
    # }
    
    # requests events {
    async def get_events(self, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', 'events')

    async def get_events_by_id(self, id: int, params: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'events/{id}')

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
        #return await self._make_request('GET', 'meetings?state=started&toDatetime=2024-11-26T23%3A00%3A00.000000&fromDatetime=2024-11-25T00%3A00%3A00.000000', data=data)


    async def create_meeting(self, params: dict = None,
                            custom_data: dict = None,
                            name_vks: str = None,
                            date_vks: str = None, 
                            duration_vks: int = None, 
                            participants_count_vks: int = None, 
                            organizer: dict = None,
                            participants: list[dict] = None) -> Optional[Any]:
        #print(participants.insert(0, organizer), participants)
        
        if custom_data is None:

            data = { 
                    "name": name_vks,
                    "comment": "string",
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
                    "backend": "cisco",
                    "createdUser": {
                        "id": 546,
                        "lastName": "Хантатонов",
                        "firstName": "Хантатон",
                        "middleName": "",
                        "roleIds": [3],
                        "departmentId": 2,
                        "email": "hantaton03.h@mail.ru"
                    },
                    "organizedUser": {
                        "id": organizer['id'],
                        "lastName": "Хантатонов",
                        "firstName": "Хантатон",
                        "middleName": None,
                        "roleIds": [3],
                        "departmentId": 2,
                        "email": "test1.b@mail.ru"
                    },
            }

        return await self._make_request('POST', 'meetings', data=data)


    async def get_meetings_by_id(self, id: int, params: dict = None, data: dict = None) -> Optional[Any]:
        return await self._make_request('GET', f'meetings/{id}', data=data)


    async def _create_meeting(
        self, 
        jwt_token: str,
        organizer_id: str,
        name_vks: str,
        date_vks: str, 
        duration_vks: int,
        participants_count_vks: int, 
        participants: list[dict],
        backend: str,
        settings: dict,
        place: str | None = None,
    ) -> Optional[Any]:
        data = {
            "name": name_vks,
            "participantsCount": participants_count_vks,
            "sendNotificationsAt": date_vks,
            "startedAt": date_vks,
            "duration": duration_vks,
            "participants": participants,
            "state": "booked",
            "backend": backend,
            "organizedBy": {
                "id": organizer_id
            }
        }
        match backend:
            case "cisco":
                data["ciscoSettings"] = settings
            case "external":
                data["externalSettings"] = settings
            case "vinteo":
                data["vinteoSettings"] = settings

        headers = {
            'Content-Type': 'application/json',
            'Authorization': "bearer " + jwt_token
        }
        if place is not None:
            data["roomId"] = place
        async with self.session.post('https://test.vcc.uriit.ru/api/meetings', json=data, headers=headers) as response:
            return {"data": await response.json(), "status": response.status}
    
    
    #Закрыть клиент при завершении работы.
    async def close(self):
        await self._client.aclose()


    async def get_buildings(self, jwt_token: str):
        headers = {
            'Authorization': "bearer " + jwt_token
        }
        async with self.session.get('https://test.vcc.uriit.ru/api/catalogs/buildings?rowsPerPage=100', headers=headers) as response:
            return {"data": await response.json(), "status": response.status}
            
    async def get_rooms(self, jwt_token: str, building_id: int):
        headers = {
            'Authorization': "bearer " + jwt_token
        }
        async with self.session.get('https://test.vcc.uriit.ru/api/catalogs/rooms?rowsPerPage=1000', headers=headers) as response:
            data =  {"data": await response.json(), "status": response.status}
        filtered_rooms = [room for room in data["data"]["data"] if room["buildingId"]==building_id]
        data["data"]["data"] = filtered_rooms
        return data
    

    async def get_user(self, jwt_token: str, email: str):
        headers = {
            'Authorization': "bearer " + jwt_token
        }
        async with self.session.get(f'https://test.vcc.uriit.ru/api/users?email={email}', headers=headers) as response:
            data =  {"data": await response.json(), "status": response.status}
        return data
    
    
    async def get_meetings(
            self, 
            jwt_token: str,
            page: int,
            date_from: str, 
            date_to: str,
            state: str,
            filters: dict = {}
        ) -> tuple[list, int]: # (meetings, rowsNumber)
        url = f'https://test.vcc.uriit.ru/api/meetings'
        headers = {
            'Authorization': "bearer " + jwt_token
        }
        params = {
            "page": page,
            "rowsPerPage": MEETINGS_ON_PAGE,
            "fromDatetime": date_from,
            "toDatetime": date_to,
            "state": state
        }
        params.update(**filters)
        async with self.session.get(url, headers=headers, params=params) as response:
            if response.ok:
                data = await response.json()
            else:
                print(response.status, 123123123123, response.json())
                raise Exception()
        return data["data"][:MEETINGS_ON_PAGE], data["rowsNumber"]
    

    async def get_departments(
            self, 
            jwt_token: str,
        ):
        headers = {
            'Authorization': "bearer " + jwt_token
        }
        
        async with self.session.get('https://test.vcc.uriit.ru/api/catalogs/departments?rowsPerPage=99', headers=headers) as response:
            data =  {"data": await response.json(), "status": response.status}
        return data