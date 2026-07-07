try:
    import pyodbc
except ImportError:
    pyodbc = None


def connect_to_database():
    if pyodbc is None:
        return None

    try:
        connection = pyodbc.connect(
            r'DRIVER={SQL Server};SERVER=DESKTOP-S70PDKD\SQLEXPRESS;DATABASE=cong_nghe_phan_mem;Trusted_Connection=True;'
        )
        print("Kết nối thành công!")
        return connection
    except Exception as e:
        print("Lỗi kết nối:", e)
        return None
