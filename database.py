import dataclasses
import sqlite3 as sq
from dataclasses import dataclass

from pprint import pprint
from typing import Any
from exceptions import DatabaseError

DATABASE_FILENAME = "database.db"
SQL_FILENAME = "database.sql"
KEYTABLE = "students"


conn = sq.connect(DATABASE_FILENAME)
conn.row_factory = sq.Row

cursor = conn.cursor()

@dataclass
class Student:
    name: str
    birthdate: str
    address: str
    phone: str
    email: str
    id: int = None

    def keys(self):
        dataclass_dict = dataclasses.asdict(self)
        dataclass_keys = dataclass_dict.keys()
        return tuple(dataclass_keys)

    def values(self):
        dataclass_dict = dataclasses.asdict(self)
        dataclass_values = dataclass_dict.values()
        return tuple(dataclass_values)
    

# tigran = Student(
#     id = -1,
#     name = "Тигран",
#     birthdate = "23.07.2002",
#     address = "Кошевого 24",
#     phone = "89062109545",
#     email = "tumb4ka228@gmail.com",
# )


def start_database(sql_filename: str = SQL_FILENAME) -> None:
    """Инициализирует базу данных по заданному SQL файлу, если она ранее не была инициализирована."""
    global SQL_FILENAME
    SQL_FILENAME = sql_filename # some wierd stuff
    if not _is_keytable_indatabase():
        _init_database(sql_filename)
        print("*Вы инициализировали базу данных*")
    else:
        print("*База данных уже инициализирована*")


def get_all_students() -> list[Student]:
    cursor.execute(f"SELECT * FROM {KEYTABLE}")
    student_rows = cursor.fetchall()
    students = list()
    for student_row in student_rows:
        student = _row_to_student(student_row)
        students.append(student)
    return students

def get_student(key, value) -> Student:
    pass

def add_student(student: Student, jentle=True, ghost=False) -> None:
    """Добавляет студента в базу данных."""

    if is_indatabase(KEYTABLE, student.name):
         print(f"[=] Студент {student.name} уже в базе данных")
         return None
    
    fields = student.keys()[:-1]    # deleting id field
    values = student.values()[:-1]
    
    try:
        cursor.execute(f"INSERT INTO {KEYTABLE} {fields} VALUES {values};") 
        print(f'[+] Студент {student.name} внесен в базу данных.')
    except:
        raise DatabaseError
    if not ghost:
        conn.commit()


def change_student(student: Student, key: str, value: Any, ghost=False) -> None:
    """Изменяет выбранное значение у студента."""               # пока хз как будет происходить идентификация
    cursor.execute(f"""
        UPDATE {KEYTABLE}
        SET "{key}" = "{value}"
        WHERE id = {student.id}
    """)
    print(f"[~] Значения студента {student.name} изменены.")
    if not ghost:
        conn.commit()


def delete_student(student: Student, ghost=False):
    """Удаляет студента из базы данных."""
    if not ghost:
        conn.commit()


def is_indatabase(table: str, value, key="name", strict=True) -> bool:
    """Checks does table contains value (defailt key is "name")"""
    if strict:
        cursor.execute(f"SELECT * FROM {table} WHERE {key} = '{value}'")
    else:
        cursor.execute(f"SELECT * FROM {table} WHERE {key} LIKE '%{value}%'")
    result = bool(cursor.fetchone())
    return result


def _is_keytable_indatabase() -> bool:
    """Проверяет есть ли целевая таблица в базе данных."""
    result = is_indatabase('sqlite_master', KEYTABLE)
    return result


def _row_to_student(student_row: sq.Row) -> Student:
    """Конвертирует sq.Row в Student"""
    student = Student(
        id = student_row["id"],
        name = student_row ["name"],
        birthdate = student_row["birthdate"],
        address = student_row["address"],
        phone = student_row["phone"],
        email = student_row["email"],
    )
    return student


def _get_sql_script(sql_filename: str = SQL_FILENAME) -> str:
    with open(sql_filename, "r") as sql_file:
        return sql_file.read()


def _init_database(sql_filename: str = SQL_FILENAME) -> None:
    """Инициализирует базу данных из SQL файла"""
    try:
        script = _get_sql_script(sql_filename)
        cursor.executescript(script)
    except:
        raise DatabaseError("Ошибка при инициализации базы данных.")


def main():
    start_database()
    students = get_all_students()

    # add_student(tigran)
    student = students[-1]

    change_student(student, 'phone', 54362)
    pprint(get_all_students())

    pass

if __name__ == "__main__":
    main()
