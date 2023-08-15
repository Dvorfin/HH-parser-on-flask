import time
from datetime import datetime
import requests
import json
from math import ceil

# professional_roles
#   27 - другое
#       40 - другое
#   116  - Специалист по информационной безопасности
#   11 - все что входит в информационнеы технологии
#       156 - BI-аналитик
#       160 - DevOps
#       10 - аналитик
#       12 - Арт-директор
#       150 - Бизнес-аналитик
#       25 - Гейм-дизайнер
#       165 - DS
#       34 - художник/дизайнер
#       36 - директор по ИТ
#       73 - менеджер продукта
#       155 - методолог
#       96 - Программист, разработчик
#       164 - Продуктовый аналитик
#       164 - Продуктовый аналитик
#       104 - Руководитель группы разработки
#       157 - Руководитель отдела аналитики
#       107 - Руководитель проектов
#       112 - Сетевой инженер
#       113 - Системный администратор
#       148 - Системный аналитик
#       114 - Системный инженер
#       116 - Специалист по информационной безопасности
#       121 - Специалист технической поддержки
#       124 - Тестировщик
#       125 - Технический директор (CTO)
#       126 - Технический писатель


class HHApi:
    def __init__(self):
        self._url = "https://api.hh.ru/vacancies"
        self._text = 'DESCRIPTION:python AND (IT OR python OR разработчик OR python стажер OR стажировка IT OR intern python OR junior python OR стажировка) AND ' \
                     'NOT (1C OR HR OR менеджер OR PHP OR Java OR JavaScript OR маркетинг OR UX OR SMM' \
                     ' OR дизайн OR закупки)'
        self._page = 0
        self._per_page = '20'
        self._search_params = {
            'text': self._text,
            'page': self._page,
            'per_page': self._per_page,
            'area': ['1', '232'],  # Москва, Центральный округ
            'experience': 'noExperience',  # опыт
            'employment': ['probation', 'full', 'part'],  # тип занятости
            'professional_roles': ['27', '40', '160', '10', '96', '112', '113',
                                   '148', '114', '116', '121', '124', '126']    # профессиональная роль | 40 - другое
        }
        self._response = None
        self._request_flag = True
        self._value_found_vacancies = 0 # общее кол-во найденных ваканский


    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self._search_params['text'] = text

    def get_value_found_vacancies(self):
        return self._value_found_vacancies

    def get_total_pages(self):
        print(self._value_found_vacancies, int(self._per_page))

        return ceil(self._value_found_vacancies / int(self._per_page))

    def make_request(self):
        try:
            self._response = requests.get(self._url, params=self._search_params)
            print(f'Request to {self._url}. Status code is {self._response.status_code}.')

            tmp = json.loads(self._response.content.decode())
            print('-' * 50)
            self._value_found_vacancies = tmp['found']
            print(f"Found {tmp['found']} vacancies with request '{self._text}'")
            print(f"Search URL: {tmp['alternate_url']}")
            print('-' * 50)

            time.sleep(0.25)
        except Exception as e:
            print(f"Can't connect to HeadHunter. Error: {e}")

    def set_page(self, page):
        self._search_params['page'] = page

    def get_data(self):  # возвращает данные в виде словаря
        return json.loads(self._response.content.decode())

    def __del__(self):
        if self._response:
            self._response.close()
            self._request_flag = True

    @classmethod
    def filter_data_from_hh(cls, data_from_hh_api):
        id = data_from_hh_api['id']  # id конкретной вакансии
        name = data_from_hh_api['name']  # название вакансии
        salary = None  # ЗП
        if data_from_hh_api['salary']:
            salary = data_from_hh_api['salary']['from'], data_from_hh_api['salary']['to']  # зп (от и до)
        vac_type = data_from_hh_api['type']['name']  # тип ваканасси (открытая/закрытая)
        published_at = HHApi.convert_time(data_from_hh_api['published_at'])
        employer = data_from_hh_api['employer']['name'], data_from_hh_api['employer'].get('alternate_url', None)  # (название компании, ссылка на компанию)
        requirement = data_from_hh_api['snippet'].get('requirement', 'None')  # требования
        responsibility = data_from_hh_api['snippet'].get('responsibility', 'None')  # обязанности
        vacancy_url = data_from_hh_api['alternate_url']  # ссылка на вакансию
        experience = data_from_hh_api['experience']['name']  # требуемый опыт
        employment = data_from_hh_api['employment']['name']  # тип вакансии: стажировка/полная/частичная занятость

        return list(map(str, [name, salary, vac_type])) + [published_at] + list(map(str, [employer, requirement, responsibility,
                         vacancy_url, experience, employment]))


    @classmethod
    def convert_time(cls, t: str):
        new_t = t[:t.rfind('+')].split('T')
        year, month, day = map(int, new_t[0].split('-'))
        h, m, s = map(int, new_t[1].split(':'))
        return datetime(year=year, day=day, month=month, hour=h, minute=m, second=s)


# 2023-06-07T12:12:51+0300

