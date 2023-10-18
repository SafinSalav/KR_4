from currency_rate import get_currency_rate


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
                if vacancy['salary']['from'] is None:
                    self.salary_from = 0
                else:
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
