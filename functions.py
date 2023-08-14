from datetime import datetime


def write_requests_into_txt(req_text):
    data = []
    with open('requests.txt', 'r', encoding='UTF-8') as file:
        data_from_file = file.readlines()
        if len(data_from_file) > 5:
            for el in data_from_file[-5:]:  # если более 5 записей, то отрезаем
                data.append(el)
        else:
            data = data_from_file

    #open('requests.txt', 'w').close()

    with open('requests.txt', 'w', encoding='UTF-8') as file:
        for el in data:
            file.write(el)  # записываем последние 5 и новый запрос
        file.write(req_text + '\n')


def get_last_request():
    with open('requests.txt', 'r', encoding='UTF-8') as file:
        data_from_file = file.readlines()
        return data_from_file[-1].strip()
