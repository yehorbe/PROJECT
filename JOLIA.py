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

def get_items():
    sql = "SELECT * FROM items;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def creat_game(start_money, p_name, p_role, cur_country):
    sql = "INSERT INTO game (money, player_name, role, location) VALUES (%s, %s, %s, %s)";
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (p_name, p_role, start_money, cur_country,))
    game_id = cursor.lastrowid
    goals = get_goals()
    goal_list = []
    for goal in goals:
        for i in range(0, goal['probability'], 1):
            goal_list.append(goal['id'])

    for i, goal_id in enumerate(goal_list):
        sql = "INSERT INTO ports (game, airport, goal) VALUES (%s, %s, %s);"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, (g_id, g_ports[i]['ident'], goal_id))
    return game_id
