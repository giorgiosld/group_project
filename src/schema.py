from db import db_context

CREATE_TABLE_STUDENT = """
CREATE TABLE IF NOT EXISTS student (
    id integer PRIMARY KEY,
    email varchar(100) UNIQUE NOT NULL,
    name varchar(12) NOT NULL,
);
"""


CREATE_TABLE_EXAMS = """
CREATE TABLE IF NOT EXISTS exams (
    id integer PRIMARY KEY,
    title varchar(24) NOT NULL,
    grade integer NOT NULL,
    user_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
"""

CLEAR_TABLE_CHALLENGE = "DELETE FROM challenges"

STUDENT_DATA = [
    Student(1, email="1nome.cognome@studenti.unicam.it", name="giorgio"),
    Student(2, email="2nome.cognome@studenti.unicam.it", name="marta"),
    Student(3, email="3nome.cognome@studenti.unicam.it", name="lorenzo"),
]

def create_db():
    with db_context() as conn:
        conn.execute(CREATE_TABLE_STUDENT)
        conn.execute(CREATE_TABLE_PA)

        #fill the tables
        for student in STUDENT_DATA:
            insert = """
                INSERT INTO users (id, email, name)
                VALUES (
                    {user.id},
                    '{user.email}',
                    '{user.name}}'
                )
            """
            conn.execute(insert)

#        for exams in range(1, 5):
