import mariadb
import random
print(mariadb.__version__)
connection = mariadb.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "root",
    password = "150102",
    database = "when_pigs_fly",
    autocommit = True
)
print("Connected!")

def get_countries():
    sql = "SELECT name, iso_country FROM country WHERE continent = EU AND iso_country != 'RU'"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def get_goals():
    sql = "SELECT * FROM goal;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result