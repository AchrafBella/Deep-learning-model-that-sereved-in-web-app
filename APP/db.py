import sqlite3
from datetime import datetime

def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file name
    :return: Connection object or None
    """
    with sqlite3.connect(db_file) as conn:
        return conn

def create_user_table(conn):
    """ create a table called CACHE
    :param conn: Connection object
    """
    with conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        username varchar(20) NOT NULL,
                                                        password varchar(20) NOT NULL)""")

def create_DL_model_table(conn):
    """ create a table called CACHE
    :param conn: Connection object
    """
    with conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS monitoring (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        model_name varchar(10),
                                                        predictions_date DATETIME,
                                                        prediction varchar(10),
                                                        error varchar(10))""")

def add_user(conn, username, password):
    """
    add user
    """
    with conn:
        conn.execute("""INSERT INTO users VALUES (NULL, @username, @password)""", 
                     {"username": username, "password": password})

def add_prediction_information(conn, model_name, prediction, error):
    """
    add model predictions 
    """
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    with conn:
        conn.execute("""INSERT INTO monitoring VALUES (NULL, @model_name, @predictions_date, @prediction, @error)""", 
                     {"model_name": model_name, "predictions_date": formatted_datetime, "prediction": prediction, "error": error})

def display_users_data(conn):
    """ view the table
    :param conn: Connection object
    """
    with conn:
        return conn.execute("""SELECT * FROM users""").fetchall()

def display_DL_model_data(conn):
    """ view the table
    :param conn: Connection object
    """
    with conn:
        return conn.execute("""SELECT * FROM monitoring""").fetchall()
    
def clear_table(conn):
    """ delete all the records in the table
    :param conn: Connection object
    """
    with conn:
        conn.execute("""DELETE FROM monitoring""")

def check_credintials(conn, username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    with conn:
        res = conn.execute(query).fetchone()
        if res:
            return True
        return False
    