from httpx import AsyncClient, codes

from src.exceptions import FailedResponseError
from src.settings import settings


class IteriosApiClient(AsyncClient):
    def __init__(self):
        super().__init__(
            base_url='https://itapi2.iterios.com/api/v1',
            headers={
                'x-iterios-api-key': settings.iterios_api_key,
            },
            timeout=60,
        )

    async def get_main_reference(self, country_iso: str, dep_city_id: int):
        response = await self.get(
            '/search/main-reference',
            params={
                'lang': 'ru',
                'country_iso': country_iso,
                'dep_city_id': dep_city_id,
            },
        )

        if response.status_code != codes.OK:
            raise FailedResponseError(response.status_code)

        return response.json()

    async def start_search(self, payload: dict):
        response = await self.post(
            '/search/start',
            json=payload,
        )

        if response.status_code != codes.OK:
            raise FailedResponseError(response.status_code)
