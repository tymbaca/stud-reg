import database
from database import Student, start_database
from pprint import pprint
from unicodedata import name
from listsplit import listsplit

from exceptions import StudParseError



def _get_raw_data(filename: str) -> str:
    """Возвращает сырой текст из целевого файла"""
    with open(filename, "r", encoding="utf-8") as file:
        raw_data = file.read()
    return raw_data


# def _split_lines(raw_data: str) -> list:
#     """Возвращает список строк из текста. Параллельно чистит от всящих пробелов."""
#     lines = raw_data.splitlines()
#     for index, line in enumerate(lines):
#         lines[index] = line.strip()
#     return lines

def _clean_lines(lines: list[str]) -> list[str]:
    """Чистит висящие пробелы"""
    for index, line in enumerate(lines):
        lines[index] = line.strip()
    return lines
    

def _raw_students(raw_data: str) -> list[list]: #переименуй _get_raw_students()
    """Возвращает список из сырых студентов (вложенные списки с данными студентов). На вход принимает сплошной текст (строку) из целевого файла."""
    lines = raw_data.splitlines()
    lines = _clean_lines(lines)
    raw_students = listsplit(lines)
    return raw_students

def _bake_students(raw_students: list[list]) -> list[Student]:
    """Возвращает список из экземпляров класса Student из сырых студентов"""
    try:
        students = []
        for student in raw_students:
            students.append(Student(
                name = student[0],
                birthdate = student[1],
                adress = student[2],
                phone = student[3],
                email = student[4],
                ))
        return students
    except:
        raise StudParseError("Неправильный формат целевого файла.")

def init_students(filename: str) -> list[Student]:
    """Возвращает список из экземпляров класса Student из исходного файла с текстом."""
    raw_data = _get_raw_data(filename)
    raw_students = _raw_students(raw_data)
    
    
    students = _bake_students(raw_students)
    
    return students


def parse_to_db() -> None:
    pass




def main():
    start_database("data.sql")
    students = init_students(filename="students.txt")
    for student in students:
        database.add_student(student)


if __name__ == "__main__":
    main()
