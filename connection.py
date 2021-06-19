import sqlite3


#CREATE DATABASE
def create_db_new():
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        first_name VARCHAR,
        step VARCHAR)''')
    sql.execute('''CREATE TABLE IF NOT EXISTS operators(
        operator_id INTEGER,
        user_id VARCHAR)''')
    sql.close()
    db.close()

#PERFORMS SQLITE3
def database_query(query: str):
    """Performs database commands.
    :params:
    query: str - this should be your command to be executed"""
    db = sqlite3.connect('users.db', check_same_thread=False)
    with db:
        sql = db.cursor()
        sql.execute(query)
        result = sql.fetchall()
    if db:
        db.commit()
        sql.close()

    return result

#PERFORMS SQLITE3
def database_query_fetchall(query: str):
    """Performs database commands.
    :params:
    query: str - this should be your command to be executed
    This function returns None if there is no such value"""
    db = sqlite3.connect('users.db', check_same_thread=False)
    with db:
        sql = db.cursor()
        sql.execute(query)
        result = sql.fetchall()
        if sql.fetchone() is None:
            return None
        else:
            return result
    if db:
        db.commit()
        sql.close()

    #return result
