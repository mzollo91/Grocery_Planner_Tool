from Grocery_Item import grocery_item
from database_manager import DatabaseManager

def main_menu():
    db = DatabaseManager()
    while True:
        print("\n--- Grocery Planner CLI ---")
        print("1. Add Item")
        print("2. View All Items")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Item Name: ")
            weight_or_count = input("Item weight or count per package: ")
            units = input("Units: ")
            department_location = input("OPTIONAL Department location in store: ")

            new_item = grocery_item(name=name, weight_or_count=weight_or_count,units=units,department_location=department_location)
            new_item.save_to_db(db)

        elif choice == '2':
            items = db.get_all_items()
            for item in items:
                print(f"{item.name} ({item.weight_or_count} {item.units})")
        elif choice == '3':
            break

main_menu()
