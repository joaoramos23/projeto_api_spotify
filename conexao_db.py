import pyodbc

def connect_db(DATABASE):
    connect_data = pyodbc.connect(
        "Driver=DRIVER-DB;"
        "Server=SERVER-DB;"
        f"Database={DATABASE};"
        "UID=USUARIO-DB;"
        "PWD=SENHA-DB", autocommit=True)
    print("Conexão Concluida!")
    return connect_data


def create_cursor(connect):
    cursor_data = connect.cursor()
    return cursor_data
