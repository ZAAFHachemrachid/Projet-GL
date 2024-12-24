import sqlite3
import os
from tkinter import messagebox

DB_FILE = "hardware_store.db"

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as err:
        messagebox.showerror("Database Error", f"Could not connect to database: {err}")
        return None

def setup_database():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        
        # Create category table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            )
        """)

        # Insert default categories if they don't exist
        default_categories = [
            ("Tools", "Hand and power tools"),
            ("Hardware", "Nuts, bolts, screws, and other fasteners"),
            ("Plumbing", "Pipes, fittings, and plumbing supplies"),
            ("Electrical", "Wiring, outlets, and electrical components"),
            ("Paint", "Interior and exterior paints and supplies"),
            ("Lumber", "Wood and building materials"),
            ("Garden", "Garden tools and supplies")
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO category (name, description) VALUES (?, ?)",
            default_categories
        )
        
        # Create products table with category_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reference TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                min_quantity INTEGER NOT NULL DEFAULT 0,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES category(id)
                    ON DELETE SET NULL
                    ON UPDATE CASCADE
            )
        """)
        
        # Create purchases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                buyer_name TEXT NOT NULL,
                total_amount REAL NOT NULL,
                purchase_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create purchase_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price_per_unit REAL NOT NULL,
                FOREIGN KEY (purchase_id) REFERENCES purchases(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        
        # Add test user if none exists
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password) 
            VALUES ('admin', 'admin123')
        """)
        
        # Add sample products with categories
        sample_products = [
            ("HM001", "Hammer - 16oz", "Standard claw hammer", 15.99, 50, 10, 1),
            ("SC002", "Screwdriver Set - 6pc", "Phillips and flathead set", 24.99, 30, 15, 1),
            ("WR003", "Adjustable Wrench - 10\"", "Adjustable wrench", 12.99, 40, 20, 1),
            ("PL004", "Pliers Set - 3pc", "Combination pliers set", 19.99, 25, 15, 1),
            ("HW001", "Assorted Screws", "Box of 100 screws", 9.99, 200, 100, 2),
            ("HW002", "Wall Anchors", "Plastic anchors, pack of 50", 5.99, 150, 75, 2),
            ("PB001", "PVC Pipe 2\"", "2-inch PVC pipe, 10 feet", 12.99, 40, 25, 3),
            ("PB002", "Pipe Wrench", "14-inch pipe wrench", 29.99, 20, 10, 3),
            ("EL001", "Wire Bundle", "14-gauge copper wire, 50 feet", 29.99, 25, 15, 4),
            ("EL002", "Outlet Box", "Single gang electrical box", 2.99, 100, 50, 4),
            ("PT001", "White Paint", "Interior latex paint, 1 gallon", 34.99, 20, 10, 5),
            ("PT002", "Paint Roller Set", "9-inch roller with tray", 14.99, 30, 20, 5),
            ("GD001", "Garden Shovel", "Steel garden shovel", 27.99, 15, 10, 7),
            ("GD002", "Pruning Shears", "Bypass pruning shears", 19.99, 25, 15, 7)
        ]
        
        cursor.executemany(
            "INSERT OR IGNORE INTO products (reference, name, description, price, quantity, min_quantity, category_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            sample_products
        )
        
        conn.commit()
        print("Database setup completed successfully")
        
    except sqlite3.Error as err:
        messagebox.showerror("Database Error", f"Error setting up database: {err}")

def get_stock_alerts():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.reference, p.name, p.quantity, p.min_quantity, c.name as category
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                WHERE p.quantity < p.min_quantity
                ORDER BY p.quantity ASC
            """)
            alerts = cursor.fetchall()
            conn.close()
            return alerts
        except sqlite3.Error as err:
            messagebox.showerror("Database Error", f"Error fetching stock alerts: {err}")
            return []
    return []

if __name__ == "__main__":
    setup_database()
