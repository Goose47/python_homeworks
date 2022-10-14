import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout, RetryError

import time


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        retries_count = 0
        start_time = time.time()
        delay = 0

        while True:
            end_time = time.time()
            time_diff = end_time - start_time
            # print(f'start_time: {start_time}')
            # print(f'end_time: {end_time}')
            # print(f'time_diff: {time_diff}')

            if retries_count > self.max_retries:
                raise RetryError
            if time_diff >= self.timeout:
                raise ReadTimeout
            time.sleep(delay)
            response = requests.get(self.base_url + url)

            if response.ok:
                return response
            else:
                delay = self.backoff_factor * (2 ** (retries_count - 1))
                retries_count += 1

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        retries_count = 0
        start_time = time.time()
        delay = 0
        payload = kwargs['payload']

        while True:
            end_time = time.time()
            time_diff = end_time - start_time
            # print(f'start_time: {start_time}')
            # print(f'end_time: {end_time}')
            # print(f'time_diff: {time_diff}')

            if retries_count > self.max_retries:
                raise RetryError
            if time_diff >= self.timeout:
                raise ReadTimeout
            time.sleep(delay)
            response = requests.get(self.base_url + url, data=payload)

            if response.ok:
                return response
            else:
                delay = self.backoff_factor * (2 ** (retries_count - 1))
                retries_count += 1
