import json
from typing import List


# открытие телефонного справочника
def open_contacts() -> List[dict]:
    with open('test.json', encoding='utf8') as f_for_read:
        all_contacts = json.load(f_for_read)
        return all_contacts


# запись в справочник
def write_contacts(all_contacts: List[dict]) -> None:
    with open('test.json', 'w', encoding='utf8') as file_for_write:
        json.dump(all_contacts, file_for_write, ensure_ascii=False, indent=4)


# создание новый контакт
def create_new_contact() -> dict:
    lastname = input('Для добавления нового контакта заполните следующие поля:\nФамилия: ')
    firstname = input('Имя: ')
    father_name = input('Отчество: ')
    company = input('Название организации: ')
    work_number = input('Рабочий телефон: ')
    private_number = input('Личный телефон: ')

    new_contact = {
        'Фамилия': lastname,
        'Имя': firstname,
        'Отчество': father_name,
        'Организация': company,
        'Рабочий-телефон': work_number,
        'Личный-телефон': private_number,
    }
    return new_contact


# отображение данных
def represent_data(list_for_render: List[dict]) -> str:
    result_str = ''
    new_line = '\n'
    for item in list_for_render:
        for key, values in item.items():
            result_str += f'{key}: {values}\n'
        result_str += '\n'
    return new_line + result_str


#  функция для постраничного отображения
def pages(list_of_contacts: List[dict]):
    number_of_contact = int(input(f'Введите число контактов на странице\nвсего контактов {len(list_of_contacts)}: '))
    number_of_pages = len(list_of_contacts) // number_of_contact
    counter = 1
    # передаем функции represent_data контакты для правильного отображения
    data_for_render = represent_data(list_of_contacts[:number_of_contact])
    print(data_for_render)
    print(f'Вы на странице {counter} всего страниц {number_of_pages}')
    while True:
        flag = int(input('Для отображения следующей странице введите 1'
                         '\nчтобы вернуться на предыдущую страницу введите 0'
                         '\nчтобы закончить просмотр введите 2: '))
        if flag == 0:
            counter -= 1
        elif flag == 1:
            counter += 1
        elif flag > 1:
            break
        contacts = list_of_contacts[number_of_contact * counter:number_of_contact * (counter + 1)]
        if len(contacts) == 0:
            print('\nВы просмотрели все контакты.')
            break
        # передаем функции represent_data контакты для правильного отображения
        data_for_render_ = represent_data(contacts)
        print(data_for_render_)
        print(f'Вы на странице {counter} всего страниц {number_of_pages}')


# определяет валидность выбора и возвращает либо False при некорректном выборе либо список с валидными ключами
def validate_choice_of_user(for_validate: List[str], correct_attributes: List[str]) -> bool | List[str]:
    user_set = set(map(lambda x: x.lower(), for_validate))
    valid_set = set(map(lambda x: x.lower(), correct_attributes))
    if valid_set >= user_set:  # на случай если пользователь ввел несколько одинаковых параметров
        return list(map(lambda x: x.title(), list(user_set)))
    else:
        return False


# создает словарь по заданным параметрам
def create_dict_by_parameters(result_choice: List[str]) -> dict | str:
    searching_dict = dict()
    for attribute in result_choice:
        if attribute == 'Фамилия' or attribute == 'Организация':
            correct_declination = attribute[:-1] + 'ю'  # делаем правильное склонение
            searching_dict[attribute] = input(f'Введите {correct_declination}: ')
        else:
            searching_dict[attribute] = input(f'Введите {attribute}: ')
    for key in searching_dict:  # проверяем все ли выбранные параметры ввел пользователь
        if len(searching_dict[key]) == 0:
            return f'Вы не заполнили параметр {key}, попробуйте еще раз.'
    return searching_dict


# определение выбора пользователя searching_changing(поиска или изменения)
def define_choice_for_searching(searching_changing: str) -> dict | str:
    attributes_list = ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий-телефон', 'Личный-телефон']
    opened_valid_list = ', '.join(attributes_list)
    user_choice = input(f'\nЧерез пробел введите параметры для {searching_changing}\n{opened_valid_list}: ').split()
    result_choice = validate_choice_of_user(user_choice, attributes_list)  # возвращает список параметров либо False
    if result_choice:
        dict_for_searching = create_dict_by_parameters(result_choice)  # создает словарь по заданным параметрам
        return dict_for_searching
    else:
        return 'Вы ввели неверные параметры, попробуйте еще раз.'
    # если функция возвращает строку то пользователь ввел не верные параметры.
    # если словарь то все в порядке


# поиск контактов по нескольким параметрам
def finding_contacts_by_attributes(list_of_contacts: List[dict], dict_for_searching: dict) -> List[dict] | str:
    list_with_found_contacts = []
    for ind in range(len(list_of_contacts)):  # обходим весь список контактов
        counter = 0  # считаем, все ли искомые параметры совпали
        for key in dict_for_searching:
            # для поиска по неполному совпадению
            if dict_for_searching[key].lower() in list_of_contacts[ind][key].lower():
                counter += 1
        if counter == len(dict_for_searching):  # проверяем, все ли искомые параметры совпали
            list_with_found_contacts.append(list_of_contacts[ind])
    if len(list_with_found_contacts) == 0:
        return 'По вашим параметрам ничего не найдено попробуйте еще раз.'
    return list_with_found_contacts


# редактирование контакта
# ПРОБНАЯ!!!!!!!!!!!!!!!!!!!!!!!
def finding_contacts_by_attributes_upd(
        list_of_contacts: List[dict], dict_for_searching: dict, flag: bool = False
) -> List | str:
    list_with_found_contacts = []
    index_ = None
    for ind in range(len(list_of_contacts)):  # обходим весь список контактов
        counter = 0  # считаем, все ли искомые параметры совпали
        for key in dict_for_searching:
            # для поиска по неполному совпадению
            if dict_for_searching[key].lower() in list_of_contacts[ind][key].lower():
                counter += 1
        if counter == len(dict_for_searching):
            list_with_found_contacts.append(list_of_contacts[ind])
            index_ = ind
            if len(list_with_found_contacts) > 1 and flag:
                return 'По вашему запросу найдено более одного контакта, пожалуйста конкретизируйте параметры,' \
                       ' за одни раз можно изменить или удалить только один контакт.\n'
    if len(list_with_found_contacts) == 0:
        return 'По вашим параметрам ничего не найдено попробуйте еще раз.'
    if flag:
        return [index_, list_with_found_contacts]
    return list_with_found_contacts


# ПРОБНАЯ!!!!!!!!!!!!!!!!!!!!!!!
# изменение контакта
def updating_contact(list_for_change: List[dict], changed_attributes: dict, index_: int) -> dict:
    for key in changed_attributes:
        list_for_change[index_][key] = changed_attributes[key]  # меняем параметры
    write_contacts(list_for_change)  # записывает измененный контакт
    return list_for_change[index_]  # выводит измененный контакт


# удаление контакта
def deleting_contact(list_for_change: List[dict], index_: int) -> dict:
    deleted_contact = list_for_change.pop(index_)
    write_contacts(list_for_change)
    return deleted_contact


# запрос начальных действий пользователя
def start() -> str:
    choice = input(
        '\nВыберете действие: '
        '\nДля добавления нового контакта введите цифру 0'
        '\nДля редактирования контакта введите цифру 1'
        '\nЧтобы найти контакт введите цифру 2'
        '\nПоказать контакты постранично, введите цифру 3'
        '\nДля удаления контакта введите цифру 4'
        '\nВаш выбор: '
    )
    return choice


# определение выбора пользователя
def define_choice(user_choice: str) -> None:
    match user_choice:

        case '0':
            new_contact = create_new_contact()  # создаем новый контакт
            all_contacts = open_contacts()  # получаем все контакты в виде списка
            all_contacts.append(new_contact)  # добавляем новый контакт
            write_contacts(all_contacts)  # записываем все контакты обратно в справочник
            print('\nВы добавили нового пользователя!')
            print(represent_data([new_contact]))  # отображаем созданный контакт для пользователя

        case '1':
            attributes_for_searching = define_choice_for_searching('поиска')
            if isinstance(attributes_for_searching, str):
                # если строка то сообщаем о том, что пользователь сделал неверный выбор
                print(attributes_for_searching)
            else:
                all_contacts = open_contacts()
                list_for_change = finding_contacts_by_attributes_upd(all_contacts, attributes_for_searching, True)
                if isinstance(list_for_change[1], str):
                    # если строка то сообщаем о том, что пользователь сделал неверный выбор
                    print(list_for_change)
                    # print('\nПо вашему запросу найдено более одного контакта, пожалуйста конкретизируйте параметры,'
                    #       ' за одни раз можно обновить только один контакт.\n')
                else:
                    print('Контакт для изменений\n')
                    print(represent_data(list_for_change[1]))
                    # index_for_change = finding_contacts_by_attributes_upd(all_contacts, attributes_for_searching, True)
                    attributes_for_changing = define_choice_for_searching('изменения')
                    if isinstance(attributes_for_changing, str):
                        # если строка то сообщаем о том, что пользователь сделал неверный выбор
                        print(attributes_for_changing)
                    else:
                        changed_contact = updating_contact(all_contacts, attributes_for_changing, list_for_change[0])
                        print('\nВы изменили контакт!')
                        print(represent_data([changed_contact]))

        case '2':
            result_of_choice = define_choice_for_searching('поиска')
            if isinstance(result_of_choice, str):
                # если строка то сообщаем о том, что пользователь сделал неверный выбор
                print(result_of_choice)
            else:
                all_contacts = open_contacts()  # получаем все контакты в виде списка
                # получаем все найденные контакты
                found_contacts = finding_contacts_by_attributes(all_contacts, result_of_choice)
                if isinstance(found_contacts, str):
                    # если строка то сообщаем о том, что пользователь сделал неверный выбор
                    print(found_contacts)
                else:
                    print(represent_data(found_contacts))  # отображаем найденные контакты

        case '3':
            all_contacts = open_contacts()  # получаем все контакты в виде списка
            pages(all_contacts)  # функция для постраничного отображения контактов

        case '4':
            attributes_for_searching = define_choice_for_searching('поиска')
            if isinstance(attributes_for_searching, str):
                # если строка то сообщаем о том, что пользователь сделал неверный выбор
                print(attributes_for_searching)
            else:
                all_contacts = open_contacts()
                list_for_change = finding_contacts_by_attributes_upd(all_contacts, attributes_for_searching, True)
                if isinstance(list_for_change[1], str):
                    # если строка то сообщаем о том, что пользователь сделал неверный выбор
                    print(list_for_change)
                    # print('\nПо вашему запросу найдено более одного контакта, пожалуйста конкретизируйте параметры,'
                    #       ' за одни раз можно обновить только один контакт.\n')
                else:
                    # print('Контакт для удаления\n')
                    # print(represent_data(list_for_change[1]))
                    deleted_contact = deleting_contact(all_contacts, list_for_change[0])
                    print('\nВы удалили контакт!')
                    print(represent_data([deleted_contact]))


if __name__ == '__main__':
    while True:
        define_choice(start())
