from Grocery_Item import grocery_item
from database_manager import DatabaseManager

def main_menu():
    db = DatabaseManager()
    while True:
        print("\n--- Grocery Planner CLI ---")
        print("1. Add Item")
        print("2. View All Items")
        print("3. Delete Item")
        print("4. Search Item")
        print("5. Exit")
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
                print(f"{item.name} ({item.weight_or_count} {item.units}), {item.department_location} department.")

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
                    print(f"{item.name} ({item.weight_or_count} {item.units}), {item.department_location} department.")
            else:
                print(f"{name} not found in database.")

        elif choice == '5':
            break

main_menu()
