from psycopg2 import connect


def create_connection():
    cnx = connect(user='postgres',
                  password='coderslab',
                  host='localhost',
                  database='expenses')

    cnx.autocommit = True
    cursor = cnx.cursor()

    return cnx, cursor


def close_connection(cnx, cursor):
    cursor.close()
    cnx.close()
