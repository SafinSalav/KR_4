import requests
import json
import os
from abc import ABC, abstractmethod


class Api(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass


class HH(Api):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies/'

    def get_vacancies(self):
        response = requests.get(self.url)
        return json.loads(response.text)


class SuperJob(Api):
    def __init__(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.Api_key = os.getenv('superjob_key')
        self.keyword = 'Python'

    @property
    def params(self):
        return {'count': 100, 'page': None, 'keyword': self.keyword, 'archive': False}

    def get_vacancies(self):
        response = requests.get(self.url, headers={'X-Api-App-Id': self.Api_key}, params=self.params)
        return json.loads(response.text)
