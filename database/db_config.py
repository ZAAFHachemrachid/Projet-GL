import mysql.connector
from tkinter import messagebox

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0000",
            database="hardware_store"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not connect to database: {err}")
        return None

def setup_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0000"
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("DROP DATABASE IF EXISTS hardware_store")
        cursor.execute("CREATE DATABASE hardware_store")
        cursor.execute("USE hardware_store")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        
        # Create category table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                description TEXT
            )
        """)

        # Insert default categories
        default_categories = [
            ("Tools", "Hand and power tools"),
            ("Hardware", "Nuts, bolts, and general hardware"),
            ("Plumbing", "Pipes and plumbing supplies"),
            ("Electrical", "Wiring and electrical supplies"),
            ("Paint", "Paint and painting supplies"),
            ("Garden", "Garden tools and supplies")
        ]
        
        cursor.executemany("""
            INSERT INTO category (name, description) 
            VALUES (%s, %s)
        """, default_categories)

        # Create products table with category_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                reference VARCHAR(50) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                quantity INT NOT NULL DEFAULT 0,
                category_id INT,
                FOREIGN KEY (category_id) REFERENCES category(id)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            )
        """)

        # Create purchases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INT AUTO_INCREMENT PRIMARY KEY,
                buyer_name VARCHAR(255) NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create purchase_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                purchase_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                price_per_unit DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (purchase_id) REFERENCES purchases(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        
        # Add test user if none exists
        cursor.execute("""
            INSERT INTO users (username, password) 
            VALUES ('admin', 'admin123')
        """)
        
        # Add sample products with categories
        sample_products = [
            ("HM001", "Hammer - 16oz", "Standard claw hammer", 15.99, 50, 1),
            ("SC002", "Screwdriver Set - 6pc", "Phillips and flathead set", 24.99, 30, 1),
            ("WR003", "Adjustable Wrench - 10\"", "Adjustable wrench", 12.99, 40, 1),
            ("PL004", "Pliers Set - 3pc", "Combination pliers set", 19.99, 25, 1),
            ("HW001", "Assorted Screws", "Box of 100 screws", 9.99, 200, 2),
            ("HW002", "Wall Anchors", "Plastic anchors, pack of 50", 5.99, 150, 2),
            ("PB001", "PVC Pipe 2\"", "2-inch PVC pipe, 10 feet", 12.99, 40, 3),
            ("PB002", "Pipe Wrench", "14-inch pipe wrench", 29.99, 20, 3),
            ("EL001", "Wire Bundle", "14-gauge copper wire, 50 feet", 29.99, 25, 4),
            ("EL002", "Outlet Box", "Single gang electrical box", 2.99, 100, 4),
            ("PT001", "White Paint", "Interior latex paint, 1 gallon", 34.99, 20, 5),
            ("PT002", "Paint Roller Set", "9-inch roller with tray", 14.99, 30, 5),
            ("GD001", "Garden Shovel", "Steel garden shovel", 27.99, 15, 6),
            ("GD002", "Pruning Shears", "Bypass pruning shears", 19.99, 25, 6)
        ]

        cursor.executemany("""
            INSERT INTO products 
            (reference, name, description, price, quantity, category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, sample_products)

        conn.commit()
        return True
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error setting up database: {err}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
