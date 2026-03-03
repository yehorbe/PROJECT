import mariadb
import random

print(mariadb.__version__)
connection = mariadb.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="150102",
    database="when_pigs_fly",
    autocommit=True
)
print("Connected!")


def get_countries():
    sql = "SELECT name, iso_country FROM country WHERE continent = 'EU' AND iso_country != 'RU'"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def show_inventory(game_id):
    sql_items = 'SELECT game_id, item_id from player_inventory where game_id = %s'
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql_items, (game_id,))
    result = cursor.fetchall()
    return result

def get_goals():
    sql = "SELECT * FROM goal;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def traveling(location):


def get_role():
    all_roles = ['thieve', 'regular', 'police']
    sql = "SELECT DISTINCT role FROM game"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    taken_roles = [row['role'] for row in results]
    available_roles = [r for r in all_roles if r not in taken_roles]
    role = random.choice(available_roles)
    return role

def get_items():
    sql = "SELECT * FROM items;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def create_game(start_money, p_name, p_role, cur_country):
    sql = "INSERT INTO game (money, player_name, role, location) VALUES (%s, %s, %s, %s);"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (start_money, p_name, p_role, cur_country))
    game_id = cursor.lastrowid

    goals = get_goals()
    goal_list = []
    for goal in goals:
        for i in range(0, goal.get('probability', 1), 1):
            goal_list.append(goal['id'])
    assigned_goal = random.choice(goal_list) if goal_list else None
    return game_id, assigned_goal



def get_player_items_count(game_id):
    sql = "SELECT COUNT(*) as count FROM player_inventory WHERE game_id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (game_id,))
    return cursor.fetchone()['count']



def buy_item(game_id, item_id, item_price):
    sql_check = "SELECT money, role FROM game WHERE id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql_check, (game_id,))
    player = cursor.fetchone()

    if player['role'] == 'thieve':
        print("Thieves cannot buy items!")
        return False

    if get_player_items_count(game_id) >= 3:
        print("LIMIT! You already have 3 items.")
        return False

    if player['money'] >= item_price:
        sql_update = "UPDATE game SET money = money - %s WHERE id = %s"
        cursor.execute(sql_update, (item_price, game_id))

        sql_insert = "INSERT INTO player_inventory (game_id, item_id) VALUES (%s, %s)"
        cursor.execute(sql_insert, (game_id, item_id))
        print("Purchased successful.")
        return True
    else:
        print("Not enough money.")
        return False



def sell_item(game_id, item_id, item_price):
    sql_delete = "DELETE FROM player_inventory WHERE game_id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql_delete, (game_id, item_id))

    if cursor.rowcount > 0:
        sql_update = "UPDATE game SET money = money + %s WHERE id = %s"
        cursor.execute(sql_update, (item_price, game_id))
        print("Sold successful.")
        return True
    else:
        print("You do not have that item.")
        return False



def steal_item(thief_id, target_player_id, item_id):
    sql_check = "SELECT role FROM game WHERE id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql_check, (thief_id,))
    sql_steal = "UPDATE player_inventory SET game_id = %s WHERE game_id = %s"
    cursor.execute(sql_steal, (thief_id, target_player_id, item_id))

    if cursor.rowcount > 0:
        print("Steal successful!")
        return True
    else:
        print("Your target does not have that item.")
        return False



def police_action(target_player_id):
    sql_check = "SELECT role FROM game WHERE id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql_check, (target_player_id,))
    target_role = cursor.fetchone()['role']

    if target_role == 'thieves':
        print("Catch!")
        return True
    elif target_role == 'regular players' or target_role == 'regular':
        print("That was regular player, you lost!")
        return False
    return False


# THE CORE GAME CODE

cursor = connection.cursor()
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("DELETE FROM game;")
cursor.execute("DELETE FROM player_inventory;")
cursor.execute("ALTER TABLE game AUTO_INCREMENT = 1;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

game_over = False
win = False
counter=0

print('So the game is starting!')
while counter!=3:
    player = input('Type your name: ')
    counter+=1

    start_country = get_countries()

    current_country = random.choice(start_country)
    money=0

    p_role=get_role()
    if p_role=='regular':
            money+=1000
    # # create_game(start_money, p_name, p_role, cur_country)
    game_creation = create_game(money, player, p_role, current_country['iso_country'])

while not game_over:
    sql_name = "SELECT player_name FROM game ORDER BY RAND() LIMIT 1"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql_name)
    result = cursor.fetchone()

    if result:
        name = result['player_name']
        print("-" * 30)
        print(f"Pass the computer to the {name}")

        sql_role = "SELECT id, role FROM game WHERE player_name = %s"
        cursor.execute(sql_role, (name,))
        result_2 = cursor.fetchone()

        if result_2:
            role=result_2['role']
            if role=='regular':
                print('So you are regular player!')

            elif role == 'thieve':
                turn_active = True
                while turn_active:
                    print("--- THIEF MENU ---")
                    command_thieves = input("Choose: [sell], [steal], [visit] or [exit] to end turn: ")
                    if command_thieves == 'sell':
                        thieve_id = result_2['id']
                        my_items = show_inventory(thieve_id)
                        if not my_items:
                            print("Your inventory is empty!")
                        else:
                            print(f"Items: {[item['item_id'] for item in my_items]}")
                            selling_item = input("Item ID to sell: ")
                            price = random.randint(100, 300)
                            answer = input(f"Sell for {price}? (Y/N): ")
                            if answer == 'Y':
                                sell_item(thieve_id, selling_item, price)
                                turn_active = False
                            else:
                                print("Sale cancelled. Choose another action.")
                    elif command_thieves == 'exit':
                        turn_active = False

                    if command_thieves=='visit':


            elif role=='police':
                print('So you are police!')
                game_over = True
            command1=input("Enter the next command: ")


