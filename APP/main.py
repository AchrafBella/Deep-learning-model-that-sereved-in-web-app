from apply_model import predictor
from db import * 
import pandas as pd
if __name__ == '__main__':
    
    conn = create_connection('database/sqlite.db')

    create_DL_model_table(conn)
    create_user_table(conn)
    
    #add_user(conn, 'admin', 'admin')

    #table = display_users_data(conn)
    #print(table)

    #v = check_credintials(conn, 'admin', 'admin')
    #print(v)

    table1 = display_DL_model_data(conn)
    columns = ['Id', 'Model_name', 'Prediction date', 'Prediction', 'Error']
    df_table = pd.DataFrame(table1, columns=columns)
    print(df_table)

    """

    img_path = os.path.join(os.getcwd(), 'APP', '0002.jpg')
    res = predictor('Model 1', img_path)
    print(res)
    """
    pass
