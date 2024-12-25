import mysql.connector
from db_config import get_db_connection

def seed_products():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # List of dummy hardware products
            products = [
                ("HM001", "Hammer - 16oz", 15.99, 50),
                ("SC002", "Screwdriver Set - 6pc", 24.99, 30),
                ("WR003", "Adjustable Wrench - 10\"", 12.99, 40),
                ("PL004", "Pliers Set - 3pc", 19.99, 25),
                ("DR005", "Power Drill - 18V", 89.99, 15),
                ("SW006", "Hand Saw - 20\"", 29.99, 20),
                ("MT007", "Measuring Tape - 25ft", 9.99, 60),
                ("LV008", "Level Tool - 24\"", 16.99, 35),
                ("CH009", "Chisel Set - 4pc", 34.99, 22),
                ("SN010", "Socket Set - 40pc", 49.99, 18),
                ("PT011", "Paint Roller Set", 11.99, 45),
                ("BR012", "Wire Brush", 7.99, 55),
                ("CK013", "Caulking Gun", 8.99, 40),
                ("GL014", "Safety Glasses", 6.99, 75),
                ("MS015", "Mason's Line - 100ft", 5.99, 65),
                ("BH016", "Bolt Cutters - 24\"", 39.99, 15),
                ("SH017", "Shovel - Round Point", 22.99, 30),
                ("RK018", "Garden Rake", 19.99, 25),
                ("AX019", "Axe - 3.5lb", 44.99, 20),
                ("WB020", "Wheelbarrow", 79.99, 10),
                ("NS021", "Nail Set - 3pc", 8.99, 50),
                ("CS022", "Circular Saw Blade - 7.25\"", 29.99, 25),
                ("HK023", "Hook and Pick Set", 14.99, 35),
                ("TG024", "Tongue and Groove Pliers", 16.99, 30),
                ("SM025", "Sledgehammer - 8lb", 34.99, 15),
                ("VP026", "Vise Grip Pliers", 21.99, 28),
                ("WG027", "Wood Glue - 16oz", 7.99, 45),
                ("ST028", "Staple Gun", 24.99, 32),
                ("CT029", "Utility Knife", 9.99, 60),
                ("TP030", "Tool Pouch", 19.99, 40)
            ]

            # Insert products
            cursor.execute("USE hardware_store")
            for product in products:
                cursor.execute("""
                    INSERT INTO products (reference, name, price, quantity)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    price = VALUES(price),
                    quantity = VALUES(quantity)
                """, product)
            
            conn.commit()
            #add admin name and password
            cursor.execute("""
                INSERT INTO users (username, password) VALUES (%s, %s)
            """, ("n", "n"))
            conn.commit()
            print("Successfully added 30 dummy products!")
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    seed_products()
