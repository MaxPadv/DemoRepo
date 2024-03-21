import inspect
import uuid
from typing import Literal, Optional

import requests
import structlog
from hamcrest import assert_that, equal_to

METHOD = Literal["get", "post", "path", "put", "delete", "head", "options"]


class CustomRestClient:
    """Абстрактный базовый класс для работы с запросами.
    Данный клиент подразумевает содержание в себе только логики отправки запросов, принятия ответов, их логирование и
    все связанное их настройкой.
    """

    session = requests.Session()

    def __init__(self, ssl_verify=False):
        """
        Args:
            ssl_verify:         верификация SSL.
        """
        self.ssl_verify = ssl_verify
        self.log = structlog.get_logger(self.__class__.__name__).bind(service="api")
        self.logger = ...

    def send_request(
        self,
        url: str,
        method: METHOD,
        params: dict = None,
        json: dict = None,
        headers=None,
        session: requests.Session = None,
        cookies=None,
        clear_cookies: bool = False,
        verify: Optional[bool] = None,
        allow_redirects: bool = True,
        auth=None,
        data=None,
        proxies=None,
        expected_status_code: int = 500,
    ) -> requests.Response:
        """Выполнить http запрос.

        Args:
            auth:               аутентификационные данные:
                                    Basic - requests.auth.HTTPBasicAuth('user', 'pass');
                                    Digest - requests.auth.HTTPDigestAuth('user', 'pass').
            url:                сформированный url для отправки http запроса.
            method:             метод запроса. [`GET`, `OPTIONS`, `HEAD`, `POST`, `PUT`, `PATCH`, `DELETE`]
            params:             query параметры запроса
            json:               словарь, который будет сериализован в JSON и передан в теле запроса.
            headers:            заголовок запроса
            session:            объект класса request.Session.
            cookies:            cookie запроса.
            clear_cookies:      очистка cookies перед выполнением запроса.
            verify:             ssl_verify: верификация SSL.
                                Параметр задокументирован в методе request() пакет requests.
            allow_redirects:    флаг указывающий на разрешение следовать редиректу.
            data:               строка, которая будет передана в теле запроса.
            proxies:
            expected_status_code: Ожидаемый статус код в ответе

        Returns:
            response:           объект класса request.Response.
        """
        if verify is None:
            verify = self.ssl_verify

        if clear_cookies:
            CustomRestClient.session.cookies.clear()

        if session:
            if headers:
                session.headers.clear()
                session.headers.update(headers)
            response = session.request(
                method=method,
                url=url,
                verify=verify,
                params=params,
                json=json,
                allow_redirects=allow_redirects,
                auth=auth,
                data=data,
                proxies=proxies,
            )
            log = self.log.bind(request_id=str(uuid.uuid4()))
        else:
            x_request_id = str(uuid.uuid4())
            if headers:
                headers.update({"X-Request-Id": x_request_id})
            else:
                headers = {"X-Request-Id": x_request_id}

            response = CustomRestClient.session.request(
                method=method,
                url=url,
                verify=verify,
                params=params,
                cookies=cookies,
                allow_redirects=allow_redirects,
                json=json,
                auth=auth,
                headers=headers,
                data=data,
                proxies=proxies,
            )

            log = self.log.bind(request_id=x_request_id)

        log.msg(
            "request",
            caller=inspect.stack()[2][3],
            method=method.upper(),
            url=url,
            json=json,
            params=params,
            data=response.request.body if response.request.body else None,
            # Корректное отображение кириллицы
            headers=dict(response.request.headers),
            proxies=proxies,
        )

        log.msg(
            "response",
            status_code=response.status_code,
            url=url,
            text=response.text,
            headers=response.headers,
            elapsed=(response.elapsed.microseconds / 1000),
        )

        assert_that(
            actual_or_assertion=response.status_code,
            matcher=equal_to(expected_status_code),
            reason=f"Ожидаемый status code: {expected_status_code} не соответствует актуальному: "
            f"{response.status_code}",
        )

        return response
