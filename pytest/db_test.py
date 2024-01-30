import sys
import os

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Get the directory of the current script
current_script_directory = os.path.dirname(current_script_path)

# Get the project root by going up one level
project_root = os.path.dirname(current_script_directory)

# Add the project root to the Python path
sys.path.append(project_root)

from APP.db import *
from pathlib import Path


def test_connection():

    create_connection('pytest/sqlite_test.db')
    db_path = Path('pytest/sqlite_test.db')

    assert db_path.is_file() == True

def test_tables_creations():

    conn = create_connection('pytest/sqlite_test.db')
    create_DL_model_table(conn)
    dl_model_table = display_DL_model_data(conn)

    create_user_table(conn)
    user_table = display_users_data(conn)

    assert len(dl_model_table) == 0 & len(user_table) == 0

def test_user_insertion():

    conn = create_connection('pytest/sqlite_test.db')
    add_user(conn, 'admin', 'admin')
    user_table = display_users_data(conn)
    clear_user_table(conn)

    assert len(user_table) == 1

def test_model_prediction_insertion():
    
    conn = create_connection('pytest/sqlite_test.db')
    add_prediction_information(conn, 'model 1', 'veg', 1)
    dl_model_table = display_DL_model_data(conn)
    clear_monitoring_table(conn)
    
    assert len(dl_model_table) == 1
