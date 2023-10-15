import json
from vacancies import Vacancy

Vacancy_list = []


def to_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


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
