from typing import Dict, Optional
<<<<<<< HEAD

import aiohttp
=======
from aiosonic import HTTPClient
>>>>>>> change-to-ruff

from x10.errors import X10Error
from x10.perpetual.accounts import StarkPerpetualAccount
from x10.perpetual.configuration import EndpointConfig
from x10.utils.http import CLIENT_TIMEOUT, get_url


class BaseModule:
    __endpoint_config: EndpointConfig
    __api_key: Optional[str]
    __stark_account: Optional[StarkPerpetualAccount]
<<<<<<< HEAD
    __session: Optional[aiohttp.ClientSession]
=======
    __client: Optional[HTTPClient]
>>>>>>> change-to-ruff

    def __init__(
        self,
        endpoint_config: EndpointConfig,
        *,
        api_key: Optional[str] = None,
        stark_account: Optional[StarkPerpetualAccount] = None,
    ):
        super().__init__()
        self.__endpoint_config = endpoint_config
        self.__api_key = api_key
        self.__stark_account = stark_account
<<<<<<< HEAD
        self.__session = None

    def _get_url(self, path: str, *, query: Optional[Dict] = None, **path_params) -> str:
        return get_url(f"{self.__endpoint_config.api_base_url}{path}", query=query, **path_params)
=======
        self.__client = None

    def _get_url(
        self, path: str, *, query: Optional[Dict] = None, **path_params
    ) -> str:
        return get_url(
            f"{self.__endpoint_config.api_base_url}{path}", query=query, **path_params
        )
>>>>>>> change-to-ruff

    def _get_endpoint_config(self) -> EndpointConfig:
        return self.__endpoint_config

    def _get_api_key(self):
        if not self.__api_key:
            raise X10Error("API key is not set")

        return self.__api_key

    def _get_stark_account(self):
        if not self.__stark_account:
            raise X10Error("Stark account is not set")

        return self.__stark_account

<<<<<<< HEAD
    async def get_session(self) -> aiohttp.ClientSession:
        if self.__session is None:
            created_session = aiohttp.ClientSession(timeout=CLIENT_TIMEOUT)
            self.__session = created_session

        return self.__session

    async def close_session(self):
        if self.__session:
            await self.__session.close()
            self.__session = None
=======
    async def get_client(self) -> HTTPClient:
        if self.__client is None:
            created_client = HTTPClient(timeout=CLIENT_TIMEOUT)
            self.__client = created_client

        return self.__client

    async def close_client(self):
        if self.__client:
            await self.__client.shutdown()
            self.__client = None
>>>>>>> change-to-ruff
