import pyodbc


def connect_to_database():
    connection_string = r'DRIVER={SQL Server};SERVER=DESKTOP-S70PDKD\SQLEXPRESS;DATABASE=cong_nghe_phan_mem;Integrated Security=SSPI;'
    return pyodbc.connect(connection_string)