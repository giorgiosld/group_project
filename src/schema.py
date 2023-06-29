from .db import db_context
from .model import Student
from random import randint

CREATE_TABLE_STUDENT = """
CREATE TABLE IF NOT EXISTS students (
    id integer PRIMARY KEY,
    email varchar(100) UNIQUE NOT NULL,
    name varchar(12) NOT NULL
);
"""


CREATE_TABLE_EXAMS = """
CREATE TABLE IF NOT EXISTS exams (
    id integer PRIMARY KEY,
    title varchar(24) NOT NULL,
    grade integer NOT NULL,
    student_id integer NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student (id)
);
"""

STUDENT_DATA = [
    Student(1, email="1nome.cognome@studenti.unicam.it", name="giorgio"),
    Student(2, email="2nome.cognome@studenti.unicam.it", name="marta"),
    Student(3, email="3nome.cognome@studenti.unicam.it", name="lorenzo"),
]

EXAMS_DATA = [
    "Advanced Programming",
    "Discrete Mathematics",
    "Mathematics Analysis"
]

def create_db():
    with db_context() as cursor:
        cursor.execute(CREATE_TABLE_STUDENT)
        cursor.execute(CREATE_TABLE_EXAMS)

        for student in STUDENT_DATA:
            insert_student = """
                INSERT INTO students (id, email, name)
                VALUES (?, ?, ?)
                """
            cursor.execute(insert_student, (student.id, student.email, student.name))
            exams_count = randint(0, 2)
            for i in range (1, exams_count):
                grade = randint(18,30)
                typo = randint(0, 2)
                insert_exam = """ 
                    INSERT INTO exams (title, grade, student_id)
                    VALUES (?, ?, ?)
                """
                cursor.execute(insert_exam, (EXAMS_DATA[typo], grade, student.id))
