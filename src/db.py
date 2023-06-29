import sqlite3
import logging
import os
import contextlib

DATABASE = os.path.realpath("/home/giorgiosld/university/bachelor/group_project/data/test.db")
logger = logging.getLogger(__name__)



def _create_connection():
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.Error:
        logger.exception("Unable to connect to database")
        raise
    else:
        return conn

@contextlib.contextmanager
def db_context():
    conn = _create_connection()
    cursor = conn.cursor()
    
    yield cursor

    conn.commit()
    cursor.close()
    conn.close()

def result_query(name):
    query = f"""
        SELECT title, grade FROM exams ex
        JOIN students s
        ON s.id = ex.student_id
        WHERE s.name='{name}';
    """
    print("-" * 50)
    print(f"Executing query: {query}")
    print("-" * 50)

    with db_context() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

        return results