from get_api import HH, SuperJob
from utils import to_json, choice_platform, sort_vacancies, Vacancy_list

to_json(HH().get_vacancies()['items'], 'HH_api.json')
to_json(SuperJob().get_vacancies()['objects'], 'SuperJob_api.json')


def main():
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


main()
