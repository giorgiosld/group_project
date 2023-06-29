import sqlite3
import logging
import os
import contextlib

DATABASE = os.path.realpath("data/test.db")
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

    cursor.close()
    conn.close()

def result_query(name):
    query = f"""
        SELECT title, grade FROM advancedprogramming pa
        JOIN student s
        ON s.id = pa.user_id
        WHERE u.name='{name}';
    """
    print("-" * 50)
    print(f"[bold]Executing query:[/bold] [green]{query}[/green]")
    print(f"[bold]{'-' * 50}[/bold]")

    with db_context() as conn:
        conn.execute(query)
        results = conn.fetchall()

        return results