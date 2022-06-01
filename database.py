import dataclasses
from shutil import ExecError
import sqlite3 as sq
from dataclasses import dataclass
from typing import Any, NamedTuple, Optional

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
    adress: str
    phone: str
    email: str
    id: Optional[int] = None      # Убрать его из вызова create_student()

    def keys(self):
        dataclass_dict = dataclasses.asdict(self)
        dataclass_keys = dataclass_dict.keys()
        return tuple(dataclass_keys)

    def values(self):
        dataclass_dict = dataclasses.asdict(self)
        dataclass_values = dataclass_dict.values()
        return tuple(dataclass_values)
    
    # _value = tuple([value for value in self])


def start_database(sql_filename: str = SQL_FILENAME) -> None:
    """Инициализирует базу данных по заданному SQL файлу, если она ранее не была инициализирована."""
    global SQL_FILENAME
    SQL_FILENAME = sql_filename # some wierd stuff
    if not _is_keytable_indatabase():
        _init_database(sql_filename)
        print("*Вы инициализировали базу данных*")
    else:
        print("*База данных уже инициализирована*")


def add_student(student: Student, jentle=True) -> None:
    """Добавляет студента в базу данных."""

    if is_indatabase(KEYTABLE, student.name):
         print(f"Студент {student.name} уже в базе данных")
         return None
    
    fields = _student_to_tuple(student)[0]
    values = _student_to_tuple(student)[1]
    
    fields = fields[:-1] # deleting id field
    values = values[:-1]
    try:
        cursor.execute(f"INSERT INTO {KEYTABLE} {fields} VALUES {values};") 
        print(f'[+] Студент {student.name} внесен в базу данных.')
    except:
        raise DatabaseError

    conn.commit()


def change_student_value(student: Student, key, value): # value_type: ValueType
    """Изменяет выбранное значение у студента."""
    cursor.execute(f"UPDATE ")

    conn.commit()


def delete_student(student: Student):
    """Удаляет студента из базы данных."""
    conn.commit()


def is_indatabase(table: str, value, key="name", strict=False) -> bool:
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


def _student_to_tuple(student: Student) -> tuple[tuple, tuple]:
    """Из экземпляра Student возвращает кортеж из двух списков -> tuple(fields, values)"""
    fields = student.keys()
    values = student.values()
    return fields, values


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
    start_database(SQL_FILENAME)
    # global jeytable init
    arman = Student(
        name='Акопян Арман Рубенович', 
        birthdate='19.10.2000', 
        adress='г. Зеленоградск ул. Ткаченко 1', 
        phone='89003471088', 
        email='metin-2014@mail.ru'
        )
    add_student(arman)


if __name__ == "__main__":
    main()
