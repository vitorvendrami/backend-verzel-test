import mysql.connector
from mysql.connector import errorcode


class DatabaseAdmin:

    @staticmethod
    def create_database():
        """Create database DB if it's not exists"""

        try:
            print("Conectando...")
            conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='password'
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Error on username or password')
            else:
                print(err)

        cursor = conn.cursor()

        cursor.execute("DROP DATABASE IF EXISTS `db`;")

        cursor.execute("CREATE DATABASE `db`;")

        cursor.execute("USE `db`;")
        print('conectado')

    @staticmethod
    def create_all_tables(db):
        try:
            db.create_all()
        except Exception as error:
            print(error)
        return "Tables created successsfully"
