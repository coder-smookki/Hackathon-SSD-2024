from typing import Any, Optional

import aiohttp

MEETINGS_ON_PAGE = 6


class AuthorizationException(Exception): ...


class UpdateTokensException(Exception): ...


class AsyncAPIClient:
    _instance: Optional["AsyncAPIClient"] = None
    session: aiohttp.ClientSession
    base_url = "https://test.vcc.uriit.ru/api/"

    def __new__(self):
        if self._instance is None:
            self._instance = super(AsyncAPIClient, self).__new__(self)
            self.session = aiohttp.ClientSession()
        return self._instance

    # Получение jwt токена для пользователя
    async def auth_login(
        self,
        login: str,
        password: str,
        params: dict = None,
    ) -> dict[str, Any]:
        data = {
            "login": login,
            "password": password,
        }

        headers = {
            "Content-Type": "application/json",  # Тип содержимого JSON
        }

        async with self.session.post(
            "https://test.vcc.uriit.ru/api/auth/login",
            json=data,
            headers=headers,
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data  # для сохранение в бд нужен не только токен
            print(f"Ошибка: {response.status}")
            raise AuthorizationException

    async def auth_logout(self, token: str):
        headers = {"Authorization": "bearer " + token}
        async with self.session.get(
            "https://test.vcc.uriit.ru/api/auth/logout",
            headers=headers,
        ) as response:
            return {"data": await response.json(), "status": response.status}

    async def update_token(self, refresh_token: str):
        headers = {
            "Content-Type": "application/json",  # Тип содержимого JSON
        }
        async with self.session.post(
            "https://test.vcc.uriit.ru/api/auth/refresh-token",
            json={"token": refresh_token},
            headers=headers,
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data  # для сохранение в бд нужен не только токен
            print(f"Ошибка: {response.status}")
            raise UpdateTokensException

    async def create_meeting(
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
    ) -> Any | None:
        data = {
            "name": name_vks,
            "participantsCount": participants_count_vks,
            "sendNotificationsAt": date_vks,
            "startedAt": date_vks,
            "duration": duration_vks,
            "participants": participants,
            "state": "booked",
            "backend": backend,
            "organizedBy": {"id": organizer_id},
        }
        match backend:
            case "cisco":
                data["ciscoSettings"] = settings
            case "external":
                data["externalSettings"] = settings
            case "vinteo":
                data["vinteoSettings"] = settings

        headers = {
            "Content-Type": "application/json",
            "Authorization": "bearer " + jwt_token,
        }
        if place is not None:
            data["roomId"] = place
        async with self.session.post(
            "https://test.vcc.uriit.ru/api/meetings",
            json=data,
            headers=headers,
        ) as response:
            try:
                data = await response.json()
            except Exception:
                data = {"detail": "Неизвестная ошибка сервера"}
            return {"data": data, "status": response.status}

    async def get_buildings(self, jwt_token: str):
        headers = {"Authorization": "bearer " + jwt_token}
        async with self.session.get(
            "https://test.vcc.uriit.ru/api/catalogs/buildings?rowsPerPage=100",
            headers=headers,
        ) as response:
            return {"data": await response.json(), "status": response.status}

    async def get_rooms(self, jwt_token: str, building_id: int):
        headers = {"Authorization": "bearer " + jwt_token}
        async with self.session.get(
            "https://test.vcc.uriit.ru/api/catalogs/rooms?rowsPerPage=1000",
            headers=headers,
        ) as response:
            data = {"data": await response.json(), "status": response.status}
        filtered_rooms = [
            room for room in data["data"]["data"] if room["buildingId"] == building_id
        ]
        data["data"]["data"] = filtered_rooms
        return data

    async def get_user(self, jwt_token: str, email: str):
        headers = {"Authorization": "bearer " + jwt_token}
        async with self.session.get(
            f"https://test.vcc.uriit.ru/api/users?email={email}",
            headers=headers,
        ) as response:
            data = {"data": await response.json(), "status": response.status}
        return data

    async def get_meetings(
        self,
        jwt_token: str,
        page: int,
        date_from: str,
        date_to: str,
        state: str,
        filters: dict = {},
    ) -> tuple[list, int]:  # (meetings, rowsNumber)
        url = "https://test.vcc.uriit.ru/api/meetings"
        headers = {"Authorization": "bearer " + jwt_token}
        params = {
            "page": page,
            "rowsPerPage": MEETINGS_ON_PAGE,
            "fromDatetime": date_from,
            "toDatetime": date_to,
            "state": state,
        }
        params.update(**filters)
        async with self.session.get(url, headers=headers, params=params) as response:
            if response.ok:
                data = await response.json()
            else:
                raise Exception
        return data["data"][:MEETINGS_ON_PAGE], data["rowsNumber"]
    
    async def get_meetings_by_id(
        self,
        jwt_token: str,
        id: int,
    ) -> tuple[list, int]:  # (meetings, rowsNumber)
        url = f"https://test.vcc.uriit.ru/api/meetings/{id}"
        headers = {"Authorization": "bearer " + jwt_token}
        # params = {
        #     "page": page,
        #     "rowsPerPage": MEETINGS_ON_PAGE,
        #     "fromDatetime": date_from,
        #     "toDatetime": date_to,
        #     "state": state,
        # }
        # params.update(**filters)
        async with self.session.get(url, headers=headers) as response:
            if response.ok:
                data = await response.json()
            else:
                raise Exception
        return data["data"][:MEETINGS_ON_PAGE], data["rowsNumber"]

    async def get_departments(
        self,
        jwt_token: str,
    ):
        headers = {"Authorization": "bearer " + jwt_token}

        async with self.session.get(
            "https://test.vcc.uriit.ru/api/catalogs/departments?rowsPerPage=99",
            headers=headers,
        ) as response:
            data = {"data": await response.json(), "status": response.status}
        return data

    # Закрыть клиент при завершении работы.
    async def close(self):
        await self._client.aclose()
