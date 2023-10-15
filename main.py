import requests
import json
import os
from abc import ABC, abstractmethod
from currency_rate import get_currency_rate

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


class Vacancy:
    def __init__(self, vacancy, platform):
        self.platform = platform
        if platform == 'HH':
            self.employer = vacancy['employer']['name']
            self.title = vacancy['name']
            self.url = vacancy['alternate_url']
            self.description = vacancy['snippet']['requirement']
            self.town = vacancy['area']['name']
            try:
                self.salary_from = vacancy['salary']['from']
            except TypeError:
                self.salary_from = 0
            try:
                self.salary_to = vacancy['salary']['to']
            except TypeError:
                self.salary_to = 0
            try:
                self.currency = vacancy['salary']['currency']
            except TypeError:
                self.currency = 'не указано'
        else:
            self.employer = vacancy['firm_name']
            self.title = vacancy['profession']
            self.url = vacancy['link']
            self.description = vacancy['candidat'][:150]
            self.town = vacancy['town']['title']
            self.salary_from = vacancy['payment_from']
            self.salary_to = vacancy['payment_to']
            self.currency = vacancy['currency']
        if self.currency.lower() not in ['rur', 'rub', 'не указано']:
            rate = round(get_currency_rate(self.currency.upper()), 2)
            if self.salary_from is not None:
                self.salary_from = f'{self.salary_from} ( {self.salary_from * rate} RUB )'
            if self.salary_to is not None:
                self.salary_to = f'{self.salary_to} ( {self.salary_to * rate} RUB )'

    def __repr__(self):
        return f'''Работодатель: {self.employer} 
Профессия: {self.title}
Ссылка: {self.url}
Описание: {self.description}
Город: {self.town}
Оплата от: {self.salary_from}
Оплата до: {self.salary_to}
Валюта: {self.currency}'''


def printj(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def to_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


to_json(HH().get_vacancies()['items'], 'HH_api.json')
to_json(SuperJob().get_vacancies()['objects'], 'SuperJob_api.json')
Vacancy_list = []


def choice_platform():
    answer_ = 0
    while answer_ not in [1, 2]:
        answer_ = int(input('''Выберете платформу поиска вакансий:
1) HH
2) SuperJob
'''))
    if answer_ == 1:
        for i in load_json('HH_api.json'):
            Vacancy_list.append(Vacancy(i, 'HH'))
    else:
        for i in load_json('SuperJob_api.json'):
            Vacancy_list.append(Vacancy(i, 'SuperJob'))


def sort_vacancies(reverse):
    salary_list = []
    for i in Vacancy_list:
        try:
            salary = int(i.salary_from)
        except ValueError:
            salary = float(list(i.salary_from.split(' '))[2])
        salary_list.append(salary)
    salary_list.sort(reverse=reverse)
    Vacancy_list_new = []
    for j in salary_list:
        for i in Vacancy_list:
            try:
                salary = int(i.salary_from)
            except ValueError:
                salary = float(list(i.salary_from.split(' '))[2])
            if salary == j:
                Vacancy_list_new.append(i)
                Vacancy_list.remove(i)
    Vacancy_list.extend(Vacancy_list_new)


def start():
    choice_platform()
    while True:
        answer = 0
        while answer not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            answer = int(input('''Выберете действие:
1) Выбрать платформу поиска вакансий
2) Ввести название профессии
3) Выбрать город
4) Вывести топ-N вакансий по зарплате
5) Отсортировать вакнсии по зарплате
6) Ввести ключевое слово
7) Вывести список вакансий
8) Сохранить вакансии в json файл
9) Выход
'''))
        if answer == 1:
            del(Vacancy_list[:])
            choice_platform()

        if answer == 2:
            answer_ = input('Введите название профессии: ')
            Vacancy_list_new = []
            for i in Vacancy_list:
                if answer_.lower() in i.title.lower():
                    Vacancy_list_new.append(i)
            if len(Vacancy_list_new) == 0:
                print(f'По запросу {answer_} ничего не найдено')
            else:
                del(Vacancy_list[:])
                Vacancy_list.extend(Vacancy_list_new)

        if answer == 3:
            answer_ = input('Введите название города: ')
            Vacancy_list_new = []
            for i in Vacancy_list:
                if answer_.lower() in i.town.lower():
                    Vacancy_list_new.append(i)
            if len(Vacancy_list_new) == 0:
                print(f'По запросу {answer_} ничего не найдено')
            else:
                del (Vacancy_list[:])
                Vacancy_list.extend(Vacancy_list_new)

        if answer == 4:
            answer_ = int(input('Вывести топ-N вакансий по зарплате (Введите N): '))
            sort_vacancies(True)
            print(f'Платформа: {Vacancy_list[0].platform}\n')
            for i in Vacancy_list[:answer_]:
                print(f'{i}\n')

        if answer == 5:
            answer_ = 0
            while answer_ not in [1, 2]:
                answer_ = int(input('''Выберете режим:
1) По возрастанию
2) По убыванию
'''))
            if answer_ == 1:
                reverse = False
            else:
                reverse = True
            sort_vacancies(reverse)

        if answer == 6:
            answer_ = input('Введите ключевое слово: ')
            super_job = SuperJob()
            super_job.keyword = answer_
            to_json(super_job.get_vacancies()['objects'], 'SuperJob_api.json')
            del (Vacancy_list[:])
            choice_platform()

        if answer == 7:
            print(f'Платформа: {Vacancy_list[0].platform}\n')
            for i in Vacancy_list:
                print(f'{i}\n')

        if answer == 8:
            answer_ = input('Введите название файла: ')
            json_list = []
            for i in Vacancy_list:
                json_list.append(i.__dict__)
            to_json(json_list, f'{answer_}.json')

        if answer == 9:
            break


start()
