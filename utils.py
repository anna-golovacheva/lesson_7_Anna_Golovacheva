import json
import re


def load_students(file_name: str) -> list[dict]:
    """
        Функция читает json-файл и преобразует его в словарь.
    """

    with open(file_name, 'r') as students:
        students_info = json.load(students)
        return students_info


def load_professions(file_name: str) -> list[dict]:
    """
        Функция читает json-файл и преобразует его в словарь.
    """

    with open(file_name, 'r') as professions:
        professions_info = json.load(professions)
        return professions_info


def get_student_by_pk(pk: int, students: list[dict]) -> dict | None:
    """
        Функция принимает уникальный ключ, введенный пользователем, и словарь,
        содержащий данные всех студентов. Возвращает словарь с данными нужного
        студента.
    """

    student = None
    for st in students:
        if st["pk"] == pk:
            student = st

    return student


def get_profession_by_title(title: str, professions: list[dict]) -> dict | None:
    """
        Функция принимает название профессии, введенное пользователем, и
        словарь, содержащий данные обо всех профессиях. Возвращает словарь с
        данными по нужной профессии.
    """

    profession = None
    for prof in professions:
        if prof["title"] == title:
            profession = prof

    return profession


def check_fitness(student_dict: dict, profession_dict: dict) -> tuple[set, set, int]:
    """
        Функция принимает словари, содержащие данные о выбранных студенте и
        профессии. Вычисляет уникальные общие скилы (какими навыками,
        необходимыми для профессии уже владеет студент), уникальные недостающие
        скилы (что еще студенту нужно изучить для данной професии), а также
        процент "подготовленности": насколько студенту подходит выбранная
        профессия, исходя из его навыков. Возвращает словарь с этими данными.
    """

    student_skills = set(student_dict['skills'])
    profession_skills = set(profession_dict['skills'])

    skills_has = student_skills.intersection(profession_skills)
    skills_lacks = profession_skills.difference(student_skills)
    skills_fit_percent = int(len(skills_has) / len(profession_skills) * 100)

    return skills_has, skills_lacks, skills_fit_percent


def check_login(login: str) -> bool:
    """
       Функция проверяет логин выбранного студента на соответствие шаблону.
    """

    is_correct = False
    pattern = r'^(?=.*[0-9])(?=.*[A-Z])(?=.*[\W_])[a-z].*[a-zA-Z0-9]$'
    result = re.match(pattern, login)
    if result:
        is_correct = True

    return is_correct


def main() -> None:
    students_info = load_students('students.json')
    professions_info = load_professions('professions.json')

    student_pk = int(input('Введите номер студента: '))

    student_dict = get_student_by_pk(student_pk, students_info)
    if not student_dict:
        print('У нас нет такого студента.')
    else:
        student_name = student_dict["full_name"]
        skills_str = ', '.join(student_dict['skills'])
        print(f'Студент {student_name}.\nЗнает {skills_str}')

        student_login = student_dict["login"]
        if check_login(student_login):
            print('У студента корректный логин. Ура!')
        else:
            print(f'У студента некорректный логин: {student_login}. Нужно исправить!')

        profession_choice = input('Выберите специальность для оценки студента Jane Snake: ').capitalize()

        profession_dict = get_profession_by_title(profession_choice, professions_info)
        if not profession_dict:
            print('У нас нет такой специальности.')
        else:
            skills_has, skills_lacks, skills_fit_percent = check_fitness(student_dict, profession_dict)
            print(f'Пригодность {skills_fit_percent}%')
            if skills_has:
                known = ', '.join(skills_has)
                print(f'{student_name} знает {known}')
            if skills_lacks:
                unknown = ', '.join(skills_lacks)
                print(f'{student_name} не знает {unknown}')


if __name__ == '__main__':
    main()
