import random
import mariadb
print(mariadb.__version__)
connection = mariadb.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="A9deazwe",
    database="when_pigs_fly",
    autocommit=True
)
print("Connected.")


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


def traveling(location, p_id):
    sql = "UPDATE game SET location = %s WHERE id = %s;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (location, p_id))
    return True


def show_all_positions():
    sql = "SELECT id, player_name, role, location FROM game ORDER BY id"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    players = cursor.fetchall()
    cursor.close()

    print("\n" + "-" * 50)
    print("Current Player Positions")
    print("-" * 50)

    if not players:
        print("No players in the game.")
        return
    for player in players:
       print(f"ID:{player['id']:<6d} Player:{player['player_name']:5s}  "
              f"Location: {player['location']:5s}")
       print("-" * 50 + "\n")

def get_role():
    all_roles = ['thief', 'regular', 'police']
    sql = "SELECT DISTINCT role FROM game"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    taken_roles = [row['role'] for row in results]
    available_roles = [r for r in all_roles if r not in taken_roles]
    role = random.choice(available_roles)
    return role

#add
def check_role(id_role):
    sql = "SELECT role FROM game WHERE id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (id_role,))
    result = cursor.fetchone()
    cursor.close()
    return result['role']


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
    sql_delete = "DELETE FROM player_inventory WHERE game_id = %s AND item_id = %s LIMIT 1"
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



def get_players_thief(thief_id, target_player_id):
    sql_locations = "SELECT id, location FROM game WHERE id IN (%s, %s)"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql_locations, (thief_id, target_player_id))
    results = cursor.fetchall()
    locations = {row['id']: row['location'] for row in results}

    if locations:
        if locations[int(thief_id)] == locations[int(target_player_id)]:
            print("You are in the same country!")
            return True
        else:
            print("You are in different countries")
            return False
    else:
        print("One of the players was not found in the database.")
        return False

#add
def get_police_thief(police_id, thief_id):
    sql_locations = "SELECT id, location FROM game WHERE id IN (%s, %s)"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql_locations, (police_id, thief_id))
    results = cursor.fetchall()
    locations = {row['id']: row['location'] for row in results}

    if locations:
        if locations[int(police_id)] == locations[int(thief_id)]:
            print("You are in the same country!")
            return True
        else:
            print("You are in different countries")
            return False
    else:
        print("One of the players was not found in the database.")
        return False


def steal_item(thief_id, target_player_id):
    cursor = connection.cursor(dictionary=True)
    if str(thief_id) == str(target_player_id):
        print("You cannot steal from yourself!")
        return False

    sql_find_item = "SELECT item_id FROM player_inventory WHERE game_id = %s ORDER BY RAND() LIMIT 1"
    cursor.execute(sql_find_item, (target_player_id,))
    item = cursor.fetchone()

    if item:
        item_id = item['item_id']
        sql_steal = "UPDATE player_inventory SET game_id = %s WHERE game_id = %s AND item_id = %s LIMIT 1"
        cursor.execute(sql_steal, (thief_id, target_player_id, item_id))
        print(f"Congrats! You've just stolen item ID:{item_id} from player {target_player_id}")
        cursor.close()
        return True
    else:
        print("There are no items with your target!")
        cursor.close()
        return False


def police_action(target_player_id):
    sql_check = "SELECT role FROM game WHERE id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql_check, (target_player_id,))
    target_role = cursor.fetchone()['role']

    if target_role == 'thief':
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
        print(f"Pass the computer to the {name}!")

        sql_role = "SELECT id, role, location FROM game WHERE player_name = %s"
        cursor.execute(sql_role, (name,))
        result_2 = cursor.fetchone()

        if result_2:
            role=result_2['role']
            show_all_positions() #add
            if role=='regular':
                print('So you are regular player!')

            elif role == 'thief':
                turn_active = True
                show_all_positions() #add
                print("--- THIEF MENU ---")
                command_thief = input("Choose: [sell], [steal], [check], [visit] or [exit] to end turn: ")

                if command_thief == 'sell':
                        thief_id = result_2['id']
                        my_items = show_inventory(thief_id)
                        if not my_items:
                            print("Your inventory is empty!")
                        else:
                            print(f"Items: {[item for item in my_items]}")
                            selling_item = input("Item ID to sell: ")
                            price = random.randint(100, 300)
                            answer = input(f"Sell for {price}? (Y/N): ")
                            if answer == 'Y':
                                sell_item(thief_id, selling_item, price)
                                turn_active = False
                            else:
                                print("Sale cancelled. Choose another action.")
                                print("~ ~ " * 13)

                elif command_thief == 'exit':
                    turn_active = False

                elif command_thief=='visit':
                        thief_id = result_2['id']
                        dest_country=input("Enter the code of the country you want to visit:")
                        traveling(dest_country, thief_id)
                        print("Have a nice trip!")
                        turn_active = False

                elif command_thief=='check':
                        thief_id = result_2['id']
                        print(f"Your ID is {thief_id}")
                        target_id=input("Enter the ID of the player you want to steal items from: ")
                        location_result=get_players_thief(thief_id, target_id)
                        print("~ ~ " * 13)

                elif command_thief == 'steal':
                        thief_id = result_2['id']
                        print(f"Your ID is {thief_id}")
                        target_id = input("Enter the ID of the player you want to steal items from: ")
                        steal_item(thief_id, target_id)
                        turn_active = False



            elif role=='police':
                show_all_positions() #add
                print('So you are police!')
                print("--- POLICE MENU ---")
                command_police = input("Choose: [check], [catch], [visit] or [exit] to end turn: ")

                if command_police == 'check':
                    police_id= result_2['id']
                    print(f"Your ID is {police_id}")
                    target_player_id = input("Enter the ID of the player you want to check: ")
                    player_check = check_role(target_player_id)
                    if player_check:
                        print(f"Player {target_player_id} is a {player_check}")
                    else:
                        print(f"Player {target_player_id} not found")
                    turn_active = False

                elif command_police == 'catch':
                    police_id = result_2['id']
                    print(f"Your ID is {police_id}")
                    target_player_id1 = input("Enter the ID of the player you want to catch: ")
                    if get_police_thief(police_id, target_player_id1):
                        if police_action(target_player_id1):
                            print("--" * 40)
                            print("Success! You caught the thief!")
                            game_over = True
                            win = True
                            print("Game Over - Police Wins!")
                        else:
                            print("--" * 40)
                            print("Failure! That was a regular player!")
                            game_over = True
                            win = False
                            print("Game Over - Police lose!")
                    else:
                        print("You must be in the same country to catch a player!")
                        print("Try visiting the target's country first.")
                    turn_active = False

                elif command_police == 'visit':
                    police_id = result_2['id']
                    dest_country = input("Enter the code of the country you want to visit:")
                    traveling(dest_country, police_id)
                    print("Have a nice trip!")
                    turn_active = False

                elif command_police == 'exit':
                    turn_active = False

