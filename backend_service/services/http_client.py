from abc import ABCMeta

import httpx
from httpx import Response
from loguru import logger


class HTTPClient(metaclass=ABCMeta):

    def __init__(self, base_url: str):
        self.base_url = base_url

        self.http_client = httpx.Client(base_url=self.base_url)

    def get(self, url: str, params: dict = None, headers: dict = None) -> Response:
        custom_headers = headers or {}
        custom_params = params or {}

        return self.http_client.get(url=url, params=custom_params, headers=custom_headers)
