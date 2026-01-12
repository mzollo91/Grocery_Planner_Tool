import pyodbc
import configparser
import os

import Grocery_Item

class DatabaseManager:
    def __init__(self,connection_string):
        self.conn_str = connection_string

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
                    return True
                except pyodbc.IntegrityError:
                    print(f"Note: {item.name} exists in the current database and was not added.")
                    return False
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    return False

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

    def delete_item(self, item_name):
        sql = """
              DELETE FROM Items WHERE ItemName = ?
              """
        params = (f"{item_name}")

        try:
            with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql,params)
                    if cursor.rowcount == 0: # cursor.rowcount doesn't give the number of rows in the db, it gives the number of rows affected by the query.
                        print(f"{item_name} does not exist in the database.")
                        return False
                    conn.commit()
                    print(f"Successfully deleted {item_name} from the database.")
                    return True
        except Exception as e:
             print(f"An unexpected error occurred: {e}")
             return False

    def search_items(self, search_term):
        from Grocery_Item import grocery_item
        sql = """
              SELECT ItemName, WeightOrCount, Units, DepartmentLocation FROM Items WHERE ItemName LIKE ?
              """
        params = (f"%{search_term}%")

        found_items=[]

        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql,params)
                    rows = cursor.fetchall()
                    for row in rows:
                        new_obj = grocery_item(row[0], row[1], row[2], row[3])
                        found_items.append(new_obj)
                    return found_items
                except pyodbc.Error as err:
                    print(f"A SQL specific error occurred: {err}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

    def insert_store(self, store):
    # Take Stores object and persists it to SQL
        sql = """
                INSERT INTO Stores (StoreName, StreetAddress, City, State, ZipCode) VALUES (?, ?, ?, ?, ?)
                """
        params = (store.name, store.street_address, store.city, store.state, store.zip_code)
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql,params)
                    conn.commit()
                    print(f"Successfully saved {store.name} to the database.")
                    return True
                except pyodbc.IntegrityError:
                    print(f"Note: {store.name} exists in the current database and was not added.")
                    return False
                except pyodbc.Error as e:
                    print(f"Database error: {e}")
                    return False

    def get_all_stores(self):
        # Fetches all rows and converts them to Stores objects
        from Stores import store

        stores = []
        sql = "SELECT StoreName, StreetAddress, City, State, ZipCode, StoreID FROM Stores"

        with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        new_obj = store(row[0], row[1], row[2], row[3], row[4], row[5])
                        stores.append(new_obj)
                    return stores