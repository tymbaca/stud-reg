from pprint import pprint
import database as db


def split_students(raw_text: str) -> list[list]:
    """Делит исходный текст на простой двухуровневый список"""
    raw_text = raw_text.replace("\n^\n", "^")
    students = raw_text.split("^")
    
    for index, student in enumerate(students):  # turple(index, value)
        students[index] = student.split("\n")
    
    return students


def bake_students(raw_text: str) -> list[db.Student]:
    """Делает список из экземпляров класса Student из исходного текста."""
    splited_students = split_students(raw_text)
    
    baked_students = []
    for student in splited_students:
        baked_students.append(db.Student(
            name = student[0],
            birthdate = student[1],
            adress = student[2],
            phone = student[3],
            email = student[4],
            ))
    
    return baked_students


def parse_to_db(raw_text: str) -> None:
    with open("students.txt", "r", encoding="utf-8") as file:
        raw_text = file.read()
    students = bake_students(raw_text)





def main():
    with open("students.txt", "r", encoding="utf-8") as file:
        raw_text = file.read()

    students = bake_students(raw_text)

    for student in students:
        pprint(student)



if __name__ == "__main__":
    main()
