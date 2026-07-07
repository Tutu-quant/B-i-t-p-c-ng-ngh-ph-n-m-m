import pyodbc
try:
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-S70PDKD\SQLEXPRESS;DATABASE=cong_nghe_phan_mem;Trusted_Connection=True;')
    print("Kết nối thành công!") 
except pyodbc.Error as e:
    print("Lỗi kết nối:", e)

cursor = connection.cursor()
