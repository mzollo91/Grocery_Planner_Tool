from Grocery_Item import grocery_item
from Stores import store_cl
from Price_Record import price_record
from database_manager import DatabaseManager
import configparser

def main_menu():

    # Load the configuration file.
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    # Create the DB connection
    db_config = config['database']
    conn_str = (f"Driver={db_config['driver']};"
                f"Server={db_config['server']};"
                f"Database={db_config['database']};"
                f"Trusted_Connection={db_config['trusted_connection']};")
    
    db = DatabaseManager(conn_str)
    
    while True:
        print("\n=== GROCERY PLANNER 2026 ===")
        print("1. Manage Items")
        print("2. Manage Stores")
        print("3. Manage Prices")
        print("Q. Exit")

        choice = input("\nSelect an option: ").lower()

        if choice == '1':
            item_submenu(db)
        elif choice == '2':
            store_submenu(db)
        elif choice == '3':
            prices_submenu(db)
        elif choice == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid selection.")
    
def item_submenu(db):
    while True:
        print("\n--- ITEM MANAGEMENT ---")
        print("1. Add Item")
        print("2. View All Items")
        print("3. Delete Item")
        print("4. Search Item")
        print("5. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Item Name: ")
            try:
                weight_or_count = float(input("Item weight or count per package: "))
            except ValueError:
                print("Invalid input, please enter a number for weight.")
                continue
            units = input("Units: ")
            department_location = input("OPTIONAL Department location in store: ")

            new_item = grocery_item(name=name, weight_or_count=weight_or_count,units=units,department_location=department_location)
            new_item.save_to_db(db)

        elif choice == '2':
            items = db.get_all_items()
            for item in items:
                print(item)
                #print(f"{item.name} ({item.weight_or_count} {item.units}), {item.department_location} department.")

        elif choice == '3':
            name = input(f"Enter the exact name of the item to delete: ")
            confirm = input(f"Are you sure want to delete '{name}'? (y/n): ")
            if confirm.lower() == 'y':
                db.delete_item(name)
            else:
                print("Deletion cancelled.")

        elif choice == '4':
            name = input("Enter item to search: ")
            found_items = db.search_items(name)
            if found_items:
                for item in found_items:
                    print(item)
            else:
                print(f"{name} not found in database.")

        elif choice == '5':
            break
        
        else:
            print("Invalid selection.")

def store_submenu(db):
    while True:
        print("\n--- STORE MANAGEMENT ---")
        print("1. Add Store")
        print("2. View All Stores")
        print("3. Delete Store")
        print("4. Search Store")
        print("5. Back to Main Menu")
        choice = input("Select an option: ").lower()

        if choice == '1':
            name = input("Store Name: ")
            street_address = input("Street Address: ")
            city = input("City: ")
            
            while True:
                state = input("State (abbrevation): ").upper()
                if len(state) == 2:
                    break
                else:
                    print("Enter the two letter abbreviation for the state.")

            zip_code = input("Zip Code: ")
            new_store = store_cl(name=name, street_address=street_address,city=city, state=state, zip_code=zip_code)
            new_store.save_to_db(db)

        elif choice == '2':
            stores = db.get_all_stores()
            for s in stores:
                print(s)

        elif choice == '3':
            name = input(f"Enter the exact name of the store to delete: ")
            confirm = input(f"Are you sure want to delete '{name}'? (y/n): ")
            if confirm.lower() == 'y':
                db.delete_store(name)
            else:
                print("Deletion cancelled.")

        elif choice == '4':
            name = input("Enter store to search: ")
            found_stores = db.search_stores(name)
            if found_stores:
                for store in found_stores:
                    print(store)
            else:
                print(f"{name} not found in database.")

        elif choice == '5':
            break

        else:
            print("Invalid selection.")

def prices_submenu(db):
    while True:
        print("\n--- PRICES MANAGEMENT ---")
        print("1. Insert/Update Price")
        print("2. View All Prices")
        print("3. Back to Main Menu")
        choice = input("Select an option: ").lower()

        if choice == '1':
            item_id = input("Enter the item ID: ")
            store_id = input("Enter the store ID: ")
            price = input("Enter the price of item: ")

            db.upsert_price(item_id, store_id, price)

        elif choice == '2':
            prices = db.get_all_prices()
            for p in prices:
                print(p)

        elif choice == '3':
            break

        else:
            print("Invalid selection.")

main_menu()
