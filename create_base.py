import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

"""
def create(user, passs, name):
    connection = psycopg2.connect(user=user, password=passs)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = cursor.execute("create database " + name)
    cursor.close()
    connection.close()"""


def create():
    connection = psycopg2.connect("dbname='kscmpkdo' user='kscmpkdo' host='batyr.db.elephantsql.com' password='Ilx0eB0taA6_qe1ihCzlJGh_7eAEXOl0'")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = cursor.execute("create database " + 'kscmpkdo')
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create()
