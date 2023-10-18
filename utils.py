from json_save import JsonSaver
from vacancies import Vacancy
from get_api import HH, SuperJob

Vacancy_list = []


def choice_platform():
    answer_ = 0
    while answer_ not in [1, 2]:
        answer_ = int(input('''Выберете платформу поиска вакансий:
1) HH
2) SuperJob
'''))
    if answer_ == 1:
        JsonSaver('HH_api.json').dump_json(HH().get_vacancies()['items'])
        for i in JsonSaver('HH_api.json').load_json():
            Vacancy_list.append(Vacancy(i, 'HH'))
    else:
        JsonSaver('SuperJob_api.json').dump_json(SuperJob().get_vacancies()['objects'])
        for i in JsonSaver('SuperJob_api.json').load_json():
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
