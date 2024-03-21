from typing import Union
from clients.api_client import CustomRestClient


class BaseRestEndpoint:
    """Базовый класс для наследования и определения поведения endpoint'ов сервисов."""

    def __init__(self, path: str, host: Union[str] = None) -> None:
        """Определить базовые параметры класса.

        Args:
            host: адрес сервиса.
            path: путь до endpoint.
        """
        self.rest_client = CustomRestClient()
        self.__host = host
        self.__path = path
        self.__headers = {}
        self.__request_bodies = {"default": None}
        self.__expected_responses = {"default": None}

    def __str__(self):
        return f'Класс: "{self.__class__.__name__}", endpoint: "{self.get_url()}"'

    def set_host(self, host):
        """Установить host сервиса."""
        self.__host = host

    def get_url(self):
        """Получить готовый url."""
        #  Костыль
        path_url = "http://157.230.31.149:9339/" + self.__path

        return path_url

    def set_headers(self, headers: dict, clear_current_headers=False):
        """Установить headers.

        Args:
            headers: словарь с headers.
            clear_current_headers: флаг необходимости очистить старые headers.

        Returns:
            dict: обновленные headers

        """
        if clear_current_headers:
            self.__headers.clear()

        self.__headers.update(headers)
        return headers

    def clear_cookies(self):
        """Очищение cookies сессии"""
        self.rest_client.session.cookies.clear()


