import MySQLdb

try:
    connection = MySQLdb.connect(
        host='localhost',
        user='Pixel_Market',
        password='Pixelmarket1',
        database='Pixel_Market',
        port=3306
    )
    print("Conexión exitosa!")
    connection.close()
except MySQLdb.Error as e:
    print(f"Error de conexión: {e}")