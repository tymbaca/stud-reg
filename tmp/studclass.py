from dataclasses import dataclass
import sqlite3

@dataclass
class Student:
    uid: int = 0
    name: str = "_empty"
    group: str = "_empty"
    phone: str = "_empty"
    email: str = "_empty"

Tigran = Student(
        uid = 1,
        name="Ростомян Тигран Меликович",
        group="1",
        phone="89062109545",
        email="tumb4ka228@gmail.com"
        )



