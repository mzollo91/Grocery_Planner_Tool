import pyodbc
import configparser
import os

import Grocery_Item

class DatabaseManager:
    def __init__(self,config_file='config.ini'):
        
        # Load the configuration file.
        config = configparser.ConfigParser()
        config.read(config_file)

        # Create the DB connection
        db_config = config['database']
        self.conn_str = (
                        f"Driver={db_config['driver']};"
                        f"Server={db_config['server']};"
                        f"Database={db_config['database']};"
                        f"Trusted_Connection={db_config['trusted_connection']};")

    def insert_item(self, item):
        # Take GroceryItem object and persists it to SQL
        sql = """
              INSERT INTO Items (ItemName, WeightOrCount, Units, DepartmentLocation) VALUES (?, ?, ?, ?)
              """
        params = (item.name, item.weight_or_count, item.units, item.department_location)
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql,params)
                    conn.commit()
                    print(f"Successfully saved {item.name} to the database.")
                except pyodbc.IntegrityError:
                    print(f"Note: {item.name} exists in the current database and was not added.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

    def get_all_items(self):
        # Fetches all rows and converts them to Grocery_Item objects
        from Grocery_Item import grocery_item

        items = []
        sql = "SELECT ItemName, WeightOrCount, Units, DepartmentLocation FROM Items"

        with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        new_obj = grocery_item(row[0], row[1], row[2], row[3])
                        items.append(new_obj)
                    return items