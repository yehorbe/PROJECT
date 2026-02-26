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
    sql = "SELECT name, iso_country FROM country WHERE continent = EU AND iso_country != 'RU'"
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


def creat_game(player_name,role):
    start_money=5000
    start_location="FI"
    sql = "INSERT INTO game (player_name, role, money, location) VALUES (%s, %s, %s, %s);
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (player_name, role, start_money, start_location))
    game_id = cursor.lastrowid
    return game_id, start_money, start_location

test_player = "TEST_PLAYER"
test_role = "regular"

game_id, money, location = creat_game(test_player, test_role)
print("game_id:", game_id)
print("Start money:", money)
print("Start location:", location)
