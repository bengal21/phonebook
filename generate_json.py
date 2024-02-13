import json
import random
from test_db import list_of_companies, list_of_all_name


# запись словаря в файл
def write_contacts(all_contacts: list[dict]) -> None:
    with open('a.json', 'w', encoding='utf8') as file_for_write:
        json.dump(all_contacts, file_for_write, ensure_ascii=False, indent=4)


# генерация словаря
def random_dict() -> dict:
    list_of_random = random.choice(list_of_all_name).split()
    new_dict = {
        "Фамилия": f"{list_of_random[0]}",
        "Имя": f"{list_of_random[1]}",
        "Отчество": f"{list_of_random[2]}",
        "Организация": f"{random.choice(list_of_companies)}",
        "Рабочий-телефон": f"{number_phone()}",
        "Личный-телефон": f"{number_phone()}"
    }
    return new_dict


# генерация номера телефона
def number_phone() -> str:
    phones = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    s = ''
    for i in range(10):
        s += str(random.choice(phones))
    return s


# функция для генерации json
def create_new_list_of_json() -> None:
    for_json = []
    try:
        number_of_json = int(input('Введите число словарей для генерации: '))
        for i in range(number_of_json):
            for_json.append(random_dict())
        write_contacts(for_json)
    except:
        print('Вы ввели не число, попробуйте еще раз.')


if __name__ == '__main__':
    create_new_list_of_json()
