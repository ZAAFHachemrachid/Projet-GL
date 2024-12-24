import customtkinter as ctk
from tkinter import ttk
import sqlite3
from database.db_config import get_db_connection

class ProductManagementFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        # Load categories
        self.categories = self.load_categories()
        
        # Create Form
        self.create_frame = ctk.CTkFrame(self)
        self.create_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.create_frame, text="Create Product", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.reference_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Product Reference")
        self.reference_entry.pack(pady=5, padx=10, fill="x")
        
        self.name_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Product Name")
        self.name_entry.pack(pady=5, padx=10, fill="x")
        
        self.description_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Description")
        self.description_entry.pack(pady=5, padx=10, fill="x")
        
        self.price_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Price")
        self.price_entry.pack(pady=5, padx=10, fill="x")
        
        self.quantity_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Quantity")
        self.quantity_entry.pack(pady=5, padx=10, fill="x")
        
        self.min_quantity_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Minimum Quantity")
        self.min_quantity_entry.pack(pady=5, padx=10, fill="x")
        
        self.category_create = ctk.CTkComboBox(self.create_frame, values=[cat[1] for cat in self.categories])
        self.category_create.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create", command=self.create_product).pack(pady=10)
        
        # Update Form
        self.update_frame = ctk.CTkFrame(self)
        self.update_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.update_frame, text="Update Product", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.update_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Product ID")
        self.update_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Load Product", command=self.load_product_for_update).pack(pady=5)
        
        self.update_reference_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Reference")
        self.update_reference_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_name_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Name")
        self.update_name_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_description_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Description")
        self.update_description_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_price_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Price")
        self.update_price_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_quantity_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Quantity")
        self.update_quantity_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_min_quantity_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Minimum Quantity")
        self.update_min_quantity_entry.pack(pady=5, padx=10, fill="x")
        
        self.category_update = ctk.CTkComboBox(self.update_frame, values=[cat[1] for cat in self.categories])
        self.category_update.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Update", command=self.update_product).pack(pady=10)
        
        # Delete Form
        self.delete_frame = ctk.CTkFrame(self)
        self.delete_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete Product", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="Product ID")
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete", command=self.delete_product, hover_color="#8679EAFF").pack(pady=10)
        
        # Products Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        columns = ('ID', 'Reference', 'Name', 'Description', 'Price', 'Quantity', 'Min Quantity', 'Category')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Refresh button
        ctk.CTkButton(self, text="Refresh Table", command=self.refresh_table).grid(row=2, column=1, pady=10)
        
        # Initial table load
        self.refresh_table()
    
    def load_categories(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM category ORDER BY name")
            categories = cursor.fetchall()
            conn.close()
            return categories
        except Exception as e:
            print(f"Error loading categories: {e}")
            return []
    
    def get_category_id(self, category_name):
        for cat_id, name in self.categories:
            if name == category_name:
                return cat_id
        return None
    
    def create_product(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            category_id = self.get_category_id(self.category_create.get())
            
            cursor.execute("""
                INSERT INTO products (reference, name, description, price, quantity, min_quantity, category_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.reference_entry.get(),
                self.name_entry.get(),
                self.description_entry.get(),
                float(self.price_entry.get()),
                int(self.quantity_entry.get()),
                int(self.min_quantity_entry.get()),
                category_id
            ))
            conn.commit()
            conn.close()
            self.clear_create_entries()
            self.refresh_table()
        except Exception as e:
            print(f"Error creating product: {e}")
    
    def update_product(self):
        try:
            # First get the existing product data
            conn = get_db_connection()
            cursor = conn.cursor()
            
            product_id = self.update_id_entry.get()
            if not product_id:
                print("Please enter a product ID")
                return
                
            # Get current product data
            cursor.execute("""
                SELECT reference, name, description, price, quantity, min_quantity, category_id
                FROM products
                WHERE id = ?
            """, (int(product_id),))
            
            current_data = cursor.fetchone()
            if not current_data:
                print("Product not found")
                return
                
            # Use new values if provided, otherwise keep current values
            new_reference = self.update_reference_entry.get() or current_data[0]
            new_name = self.update_name_entry.get() or current_data[1]
            new_description = self.update_description_entry.get() or current_data[2]
            new_price = self.update_price_entry.get()
            new_price = float(new_price) if new_price else current_data[3]
            new_quantity = self.update_quantity_entry.get()
            new_quantity = int(new_quantity) if new_quantity else current_data[4]
            new_min_quantity = self.update_min_quantity_entry.get()
            new_min_quantity = int(new_min_quantity) if new_min_quantity else current_data[5]
            
            # Handle category
            selected_category = self.category_update.get()
            new_category_id = self.get_category_id(selected_category) if selected_category else current_data[6]
            
            cursor.execute("""
                UPDATE products
                SET reference = ?, name = ?, description = ?, price = ?, quantity = ?, min_quantity = ?, category_id = ?
                WHERE id = ?
            """, (
                new_reference,
                new_name,
                new_description,
                new_price,
                new_quantity,
                new_min_quantity,
                new_category_id,
                int(product_id)
            ))
            
            conn.commit()
            conn.close()
            self.clear_update_entries()
            self.refresh_table()
            print("Product updated successfully")
        except Exception as e:
            print(f"Error updating product: {e}")

    def load_product_for_update(self):
        try:
            product_id = self.update_id_entry.get()
            if not product_id:
                print("Please enter a product ID")
                return
                
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT p.reference, p.name, p.description, p.price, p.quantity, p.min_quantity, c.name
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                WHERE p.id = ?
            """, (int(product_id),))
            
            product = cursor.fetchone()
            if not product:
                print("Product not found")
                return
            
            # Populate the update form fields
            self.update_reference_entry.delete(0, 'end')
            self.update_reference_entry.insert(0, product[0])
            
            self.update_name_entry.delete(0, 'end')
            self.update_name_entry.insert(0, product[1])
            
            self.update_description_entry.delete(0, 'end')
            self.update_description_entry.insert(0, product[2])
            
            self.update_price_entry.delete(0, 'end')
            self.update_price_entry.insert(0, str(product[3]))
            
            self.update_quantity_entry.delete(0, 'end')
            self.update_quantity_entry.insert(0, str(product[4]))
            
            self.update_min_quantity_entry.delete(0, 'end')
            self.update_min_quantity_entry.insert(0, str(product[5]))
            
            if product[6]:  # If category exists
                self.category_update.set(product[6])
            
            conn.close()
            print("Product loaded successfully")
        except Exception as e:
            print(f"Error loading product: {e}")

    def delete_product(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (int(self.delete_id_entry.get()),))
            conn.commit()
            conn.close()
            self.delete_id_entry.delete(0, 'end')
            self.refresh_table()
        except Exception as e:
            print(f"Error deleting product: {e}")
    
    def refresh_table(self):
        # Clear the table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch and display products
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.reference, p.name, p.description, p.price, p.quantity, p.min_quantity, c.name
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                ORDER BY p.id
            """)
            products = cursor.fetchall()
            
            for product in products:
                self.tree.insert('', 'end', values=product)
            
            conn.close()
        except Exception as e:
            print(f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        self.reference_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.min_quantity_entry.delete(0, 'end')
        if self.categories:
            self.category_create.set(self.categories[0][1])
    
    def clear_update_entries(self):
        self.update_id_entry.delete(0, 'end')
        self.update_reference_entry.delete(0, 'end')
        self.update_name_entry.delete(0, 'end')
        self.update_description_entry.delete(0, 'end')
        self.update_price_entry.delete(0, 'end')
        self.update_quantity_entry.delete(0, 'end')
        self.update_min_quantity_entry.delete(0, 'end')
        if self.categories:
            self.category_update.set(self.categories[0][1])
