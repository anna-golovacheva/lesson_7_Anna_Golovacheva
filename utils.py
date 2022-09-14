import json


def load_students(file_name):
    """
        Функция читает json-файл и преобразует его в словарь.
    """
    with open(file_name, 'r') as students:
        students_info = json.load(students)
        return students_info


def load_professions(file_name):
    """
        Функция читает json-файл и преобразует его в словарь.
    """
    with open(file_name, 'r') as professions:
        professions_info = json.load(professions)
        return professions_info


def get_student_by_pk(pk, students):
    """
        Функция принимает уникальный ключ, введенный пользователем, и словарь,
        содержащий данные всех студентов. Возвращает словарь с данными нужного
        студента.
    """
    students_dict = {}
    for student in students:
        if student["pk"] == pk:
            for k, v in student.items():
                students_dict[k] = v
    return students_dict


def get_profession_by_title(title, professions):
    """
        Функция принимает название профессии, введенное пользователем, и
        словарь, содержащий данные обо всех профессиях. Возвращает словарь с
        данными по нужной профессии.
    """
    professions_dict = {}
    for profession in professions:
        if profession["title"] == title:
            for k, v in profession.items():
                professions_dict[k] = v
    return professions_dict


def check_fitness(student_dict_, profession_dict_):
    """
        Функция принимает словари, содержащие данные о выбранных студенте и
        профессии. Вычисляет уникальные общие скилы (какими навыками,
        необходимыми для профессии уже владеет студент), уникальные недостающие
        скилы (что еще студенту нужно изучить для данной професии), а также
        процент "подготовленности": насколько студенту подходит выбранная
        профессия, исходя из его навыков. Возвращает словарь с этими данными.
    """
    skills_dict = {}
    student_skills = set(student_dict_['skills'])
    profession_skills = set(profession_dict_['skills'])
    skills_dict['has'] = list(student_skills.intersection(profession_skills))
    skills_dict['lacks'] = list(profession_skills.difference(student_skills))
    skills_dict['fit_percent'] = int(len(skills_dict['has']) / len(profession_skills) * 100)
    return skills_dict


def main():
    students_info_ = load_students('students.json')
    professions_info_ = load_professions('professions.json')

    students_info_ = load_students('students.json')
    professions_info_ = load_professions('professions.json')

    student_pk = int(input('Введите номер студента: '))

    student_dict_ = get_student_by_pk(student_pk, students_info_)
    if not student_dict_:
        print('У нас нет такого студента.')
    else:
        skills_str = ', '.join(student_dict_['skills'])
        print(f'Студент {student_dict_["full_name"]}.\nЗнает {skills_str}')

        profession_choice = input('Выберите специальность для оценки студента Jane Snake: ').capitalize()

        profession_dict_ = get_profession_by_title(profession_choice, professions_info_)
        if not profession_dict_:
            print('У нас нет такой специальности.')
        else:
            student_skills_in_profession_dict = check_fitness(student_dict_, profession_dict_)
            print(f'Пригодность {student_skills_in_profession_dict["fit_percent"]}%')
            if student_skills_in_profession_dict['has']:
                known = ', '.join(student_skills_in_profession_dict['has'])
                print(f'{student_dict_["full_name"]} знает {known}')
            if student_skills_in_profession_dict['lacks']:
                unknown = ', '.join(student_skills_in_profession_dict['lacks'])
                print(f'{student_dict_["full_name"]} не знает {unknown}')

main()