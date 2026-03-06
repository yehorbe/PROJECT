if role == 'regular' :

    turn_active = True
    print("--- MERCHANT MENU ---")

    while turn_active:
        regular_id = result_2 ['id']
        current_location = result_2 ['location']

        command_regular = input("Choose: [buy], [sell], [inventory], [visit] or [exit] to end turn: ")


        if command_regular=='buy':
            print(f"Yor are currently in {current_location}")

            sql= "SELECT id,name FROM items WHERE origin = %s"
            cursor.execute(sql,(location,))
            available_items=cursor.fetchall()
            print("Items available here:")

            for item in available_items:
                print(f"Item ID: {item['id']} | Name: {item['name']}")

            item_id=input("Enter item ID you want to buy: ")
            price = random.randint(100,300)
            answer= input(f"Do you want to buy it for {price} euros? (Y/N): ")

            if answer == 'Y':
                buy_item(regular_id, item_id, price)
                turn_active = False

            else:
                print("Purchase cancelled. Choose another action.")
                print("~ ~ " * 13)



        elif command_regular == 'sell' :

            my_items = show_inventory(regular_id)

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

        elif command_regular == 'inventory':

            items = show_inventory(regular_id)

            print(items)


        elif command_regular == 'visit':

            dest_country = input("Enter the code of the country you want to visit: ")
            traveling(dest_country, regular_id)
            print("Have a nice trip!")
            turn_active = False

        elif command_regular == 'exit':

            turn_active = False
