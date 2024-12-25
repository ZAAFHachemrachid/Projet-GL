import customtkinter as ctk
from tkinter import ttk, messagebox
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database.db_config import get_db_connection

class SearchProductFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.conn = get_db_connection()
        if not self.conn:
            messagebox.showerror("Error", "Could not connect to database")
            return
        
        title = ctk.CTkLabel(
            self,
            text="Search Products",
            font=("Arial", 24, "bold"),
            text_color="#333333"
        )
        title.pack(pady=20)
        
        # Search section
        self.create_search_section()
        
        # Products list
        self.create_products_list()
        
        # Load initial data
        self.load_products()
    
    def create_search_section(self):
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))
        
        # Search inputs frame
        inputs_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        inputs_frame.pack(fill="x")
        
        # Search input
        self.search_entry = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Search by product name or reference...",
            width=400
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        # Price range
        self.min_price_entry = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Min Price",
            width=150
        )
        self.min_price_entry.pack(side="left", padx=(0, 10))
        
        self.max_price_entry = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Max Price",
            width=150
        )
        self.max_price_entry.pack(side="left", padx=(0, 10))
        
        # Search button
        search_btn = ctk.CTkButton(
            inputs_frame,
            text="Search",
            fg_color="#6c5ce7",
            hover_color="#5b4cc7",
            width=100,
            command=self.search_products
        )
        search_btn.pack(side="left")
        
        # Reset button
        reset_btn = ctk.CTkButton(
            inputs_frame,
            text="Reset",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            width=100,
            command=self.reset_search
        )
        reset_btn.pack(side="left", padx=(10, 0))
    
    def create_products_list(self):
        list_frame = ctk.CTkFrame(self, fg_color="transparent")
        list_frame.pack(fill="both", expand=True)
        
        # Create treeview
        columns = ("ID", "Reference", "Name", "Category", "Price", "Quantity", "Actions")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Configure columns
        column_widths = {
            "ID": 50,
            "Reference": 100,
            "Name": 200,
            "Category": 100,
            "Price": 80,
            "Quantity": 80,
            "Actions": 100
        }
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=column_widths.get(col, 100))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_item_double_click)
    
    def load_products(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT p.id, p.reference, p.name, c.name, p.price, p.quantity 
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                ORDER BY p.name
            """)
            products = cursor.fetchall()
            cursor.close()
            
            self.update_products_list(products)
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading products: {str(e)}")
    
    def search_products(self):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT p.id, p.reference, p.name, c.name, p.price, p.quantity 
                FROM products p
                LEFT JOIN category c ON p.category_id = c.id
                WHERE 1=1
            """
            params = []
            
            # Search term filter
            search_term = self.search_entry.get().strip()
            if search_term:
                query += """ AND (
                    LOWER(p.name) LIKE LOWER(%s) OR 
                    LOWER(p.reference) LIKE LOWER(%s) OR
                    LOWER(IFNULL(c.name, '')) LIKE LOWER(%s)
                )"""
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern] * 3)
            
            # Price range filter
            min_price = self.min_price_entry.get().strip()
            if min_price:
                try:
                    min_price = float(min_price)
                    query += " AND p.price >= %s"
                    params.append(min_price)
                except ValueError:
                    messagebox.showwarning("Invalid Input", "Please enter a valid minimum price")
                    return
            
            max_price = self.max_price_entry.get().strip()
            if max_price:
                try:
                    max_price = float(max_price)
                    query += " AND p.price <= %s"
                    params.append(max_price)
                except ValueError:
                    messagebox.showwarning("Invalid Input", "Please enter a valid maximum price")
                    return
            
            query += " ORDER BY p.name"
            cursor.execute(query, params)
            products = cursor.fetchall()
            cursor.close()
            
            self.update_products_list(products)
            
        except Exception as e:
            messagebox.showerror("Search Error", f"Error searching products: {str(e)}")
    
    def update_products_list(self, products):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert products
        for product in products:
            id_, reference, name, category, price, quantity = product
            self.tree.insert("", "end", values=(
                id_,
                reference,
                name,
                category if category else "Uncategorized",
                f"${price:.2f}",
                quantity,
                "Edit | Delete"
            ))
    
    def reset_search(self):
        self.search_entry.delete(0, 'end')
        self.min_price_entry.delete(0, 'end')
        self.max_price_entry.delete(0, 'end')
        self.load_products()
    
    def sort_treeview(self, col):
        """Sort treeview when column header is clicked"""
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children("")]
        
        # Sort items
        items.sort(reverse=hasattr(self, "sort_reverse") and self.sort_reverse)
        
        # Rearrange items in sorted positions
        for index, (_, item) in enumerate(items):
            self.tree.move(item, "", index)
        
        # Switch sort order for next time
        self.sort_reverse = not hasattr(self, "sort_reverse") or not self.sort_reverse
    
    def on_item_double_click(self, event):
        """Handle double-click on item"""
        item = self.tree.selection()[0]
        item_id = self.tree.item(item)["values"][0]
        messagebox.showinfo("Product Details", f"Opening details for product {item_id}")
        # TODO: Implement product details view
