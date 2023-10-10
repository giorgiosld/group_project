'''
@uthor: Giorgio Saldana @email: giorgio.saldana@studenti.unicam.it

Questo file contiene la connesione da parte del db con il servizio SQL all'interno di un host,
definisce anche il comando relativo alla DQL

'''
import sqlite3
import logging
import os
import contextlib

DATABASE = os.path.realpath("/home/giorgiosld/university/bachelor/group_project/data/test.db")
logger = logging.getLogger(__name__)

# crea la connessione al database sqlite3, ovvero un databse installato con l'instllazione di python3
def _create_connection():
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.Error:
        logger.exception("Unable to connect to database")
        raise
    else:
        return conn

# definisce lo scope della connessione del DB, funge da wrapper per l'operazione implementata precedentemente
@contextlib.contextmanager
def db_context():
    conn = _create_connection()
    cursor = conn.cursor()
    
    yield cursor

    conn.commit()
    cursor.close()
    conn.close()

# esegue la query all'interno del DB, questa query può essere vittima di SQLi
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