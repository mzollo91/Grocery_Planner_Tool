from Grocery_Item import grocery_item
from database_manager import DatabaseManager

db = DatabaseManager()

bread = grocery_item("Sandwich Bread", 24, "oz", "Bakery")
skim_milk = grocery_item("Skim Milk", 128, "fl-oz", "Dairy")

bread.save_to_db(db)
skim_milk.save_to_db(db)
