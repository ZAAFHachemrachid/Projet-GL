import customtkinter as ctk
from tkinter import ttk, messagebox
from database.db_config import get_db_connection

class CheckoutFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.cart_items = []  # List to store cart items
        
        # Configure grid
        self.grid_columnconfigure(0, weight=3)  # Products list (wider)
        self.grid_columnconfigure(1, weight=2)  # Cart (narrower)
        self.grid_rowconfigure(1, weight=1)  # Purchase history section
        
        # Left side - Products List
        self.products_frame = ctk.CTkFrame(self)
        self.products_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Products title
        ctk.CTkLabel(
            self.products_frame,
            text="Available Products",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        
        # Products table
        columns = ('ID', 'Name', 'Price', 'Stock')
        self.products_tree = ttk.Treeview(self.products_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=100)
        
        self.products_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Add to cart frame
        add_frame = ctk.CTkFrame(self.products_frame)
        add_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(add_frame, text="Quantity:").pack(side="left", padx=5)
        self.quantity_entry = ctk.CTkEntry(add_frame, width=100)
        self.quantity_entry.pack(side="left", padx=5)
        self.quantity_entry.insert(0, "1")
        
        ctk.CTkButton(
            add_frame,
            text="Add to Cart",
            command=self.add_to_cart
        ).pack(side="left", padx=5)
        
        # Right side - Cart
        self.cart_frame = ctk.CTkFrame(self)
        self.cart_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Cart title
        ctk.CTkLabel(
            self.cart_frame,
            text="Shopping Cart",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        
        # Cart table
        cart_columns = ('Name', 'Quantity', 'Price', 'Total')
        self.cart_tree = ttk.Treeview(self.cart_frame, columns=cart_columns, show='headings')
        
        # Define cart headings
        for col in cart_columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100)
        
        self.cart_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Remove from cart button
        ctk.CTkButton(
            self.cart_frame,
            text="Remove Selected Item",
            command=self.remove_from_cart,
            fg_color="#ff9800",
            hover_color="#f57c00"
        ).pack(pady=5)
        
        # Total amount label
        self.total_label = ctk.CTkLabel(
            self.cart_frame,
            text="Total: $0.00",
            font=("Arial", 16, "bold")
        )
        self.total_label.pack(pady=5)
        
        # Buyer name entry
        self.buyer_name = ctk.CTkEntry(
            self.cart_frame,
            placeholder_text="Buyer Name"
        )
        self.buyer_name.pack(pady=5, padx=10, fill="x")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.cart_frame, fg_color="transparent")
        buttons_frame.pack(pady=10, fill="x")
        
        # Purchase button
        ctk.CTkButton(
            buttons_frame,
            text="Complete Purchase",
            command=self.complete_purchase,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(side="left", padx=5, expand=True)
        
        # Cancel button
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self.cancel_purchase,
            fg_color="#ff5252",
            hover_color="#ff0000"
        ).pack(side="left", padx=5, expand=True)
        
        # Purchase History Section
        history_frame = ctk.CTkFrame(self)
        history_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            history_frame,
            text="Purchase History",
            font=("Arial", 20, "bold")
        ).pack(pady=10)
        
        # Purchase history table
        history_columns = ('ID', 'Buyer', 'Date', 'Total Amount', 'Items')
        self.history_tree = ttk.Treeview(history_frame, columns=history_columns, show='headings')
        
        # Define history headings
        for col in history_columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=150)
        
        self.history_tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Refresh history button
        ctk.CTkButton(
            history_frame,
            text="Refresh History",
            command=self.refresh_history
        ).pack(pady=10)
        
        # Load initial data
        self.refresh_products()
        self.refresh_history()
    
    def refresh_products(self):
        # Clear current items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, price, quantity
                FROM products
                WHERE quantity > 0
                ORDER BY name
            """)
            
            for row in cursor.fetchall():
                self.products_tree.insert('', 'end', values=row)
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading products: {e}")
    
    def add_to_cart(self):
        selected_item = self.products_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product")
            return
        
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                messagebox.showwarning("Warning", "Quantity must be positive")
                return
            
            # Get product details
            product_values = self.products_tree.item(selected_item[0])['values']
            product_id = product_values[0]
            product_name = product_values[1]
            product_price = float(product_values[2])  # Convert price to float
            available_stock = int(product_values[3])  # Convert stock to int
            
            if quantity > available_stock:
                messagebox.showwarning("Warning", "Not enough stock available")
                return
            
            # Check if item already in cart
            for item in self.cart_items:
                if item['id'] == product_id:
                    new_quantity = item['quantity'] + quantity
                    if new_quantity > available_stock:
                        messagebox.showwarning("Warning", "Not enough stock available")
                        return
                    item['quantity'] = new_quantity
                    self.update_cart_display()
                    return
            
            # Add new item to cart
            self.cart_items.append({
                'id': product_id,
                'name': product_name,
                'quantity': quantity,
                'price': product_price
            })
            
            self.update_cart_display()
            
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid quantity")
    
    def update_cart_display(self):
        # Clear current cart display
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Update cart items display
        total = 0.0  # Initialize as float
        for item in self.cart_items:
            item_total = float(item['quantity']) * float(item['price'])  # Convert to float
            total += item_total
            self.cart_tree.insert('', 'end', values=(
                item['name'],
                item['quantity'],
                f"${float(item['price']):.2f}",
                f"${item_total:.2f}"
            ))
        
        # Update total
        self.total_label.configure(text=f"Total: ${total:.2f}")
    
    def complete_purchase(self):
        if not self.cart_items:
            messagebox.showwarning("Warning", "Cart is empty")
            return
        
        buyer_name = self.buyer_name.get()
        if not buyer_name:
            messagebox.showwarning("Warning", "Please enter buyer name")
            return
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Calculate total amount
            total_amount = sum(item['quantity'] * item['price'] for item in self.cart_items)
            
            # Create purchase record
            cursor.execute("""
                INSERT INTO purchases (buyer_name, total_amount)
                VALUES (?, ?)
            """, (buyer_name, total_amount))
            
            purchase_id = cursor.lastrowid
            
            # Add purchase items and update stock
            for item in self.cart_items:
                # Add purchase item
                cursor.execute("""
                    INSERT INTO purchase_items (purchase_id, product_id, quantity, price_per_unit)
                    VALUES (?, ?, ?, ?)
                """, (purchase_id, item['id'], item['quantity'], item['price']))
                
                # Update stock
                cursor.execute("""
                    UPDATE products
                    SET quantity = quantity - ?
                    WHERE id = ?
                """, (item['quantity'], item['id']))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Purchase completed successfully")
            self.cancel_purchase()  # Clear cart
            self.refresh_products()  # Refresh product list
            
        except Exception as e:
            messagebox.showerror("Error", f"Error completing purchase: {e}")
    
    def cancel_purchase(self):
        self.cart_items = []
        self.buyer_name.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.quantity_entry.insert(0, "1")
        self.update_cart_display()
    
    def remove_from_cart(self):
        selected_item = self.cart_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        # Get the name of the selected item
        item_name = self.cart_tree.item(selected_item[0])['values'][0]
        
        # Remove the item from cart_items
        self.cart_items = [item for item in self.cart_items if item['name'] != item_name]
        
        # Update the display
        self.update_cart_display()
    
    def refresh_history(self):
        # Clear current history
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get all purchases with their items
            cursor.execute("""
                SELECT p.id, p.buyer_name, p.purchase_date, p.total_amount,
                       GROUP_CONCAT(pr.name || ' (x' || pi.quantity || ')') as items
                FROM purchases p
                LEFT JOIN purchase_items pi ON p.id = pi.purchase_id
                LEFT JOIN products pr ON pi.product_id = pr.id
                GROUP BY p.id
                ORDER BY p.purchase_date DESC
            """)
            
            for row in cursor.fetchall():
                # Format the date
                purchase_date = row[2].split('.')[0]  # Remove milliseconds
                # Format total amount
                total_amount = f"${float(row[3]):.2f}"
                # Format items list
                items = row[4] if row[4] else "No items"
                
                self.history_tree.insert('', 'end', values=(
                    row[0],          # ID
                    row[1],          # Buyer name
                    purchase_date,    # Date
                    total_amount,     # Total amount
                    items            # Items list
                ))
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing purchase history: {e}")
