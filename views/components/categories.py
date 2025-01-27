import customtkinter as ctk
from tkinter import ttk, messagebox
from database.db_config import get_db_connection

class CategoriesFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        # Create Form
        self.create_frame = ctk.CTkFrame(self)
        self.create_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.create_frame, text="Create Category", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.name_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Category Name")
        self.name_entry.pack(pady=5, padx=10, fill="x")
        
        self.description_entry = ctk.CTkEntry(self.create_frame, placeholder_text="Description")
        self.description_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.create_frame, text="Create", command=self.create_category).pack(pady=10)
        
        # Update Form
        self.update_frame = ctk.CTkFrame(self)
        self.update_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.update_frame, text="Update Category", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.update_id_entry = ctk.CTkEntry(self.update_frame, placeholder_text="Category ID")
        self.update_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Load Category", command=self.load_category).pack(pady=5)
        
        self.update_name_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Name")
        self.update_name_entry.pack(pady=5, padx=10, fill="x")
        
        self.update_description_entry = ctk.CTkEntry(self.update_frame, placeholder_text="New Description")
        self.update_description_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.update_frame, text="Update", command=self.update_category).pack(pady=10)
        
        # Delete Form
        self.delete_frame = ctk.CTkFrame(self)
        self.delete_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.delete_frame, text="Delete Category", font=("Arial", 16, "bold")).pack(pady=5)
        
        self.delete_id_entry = ctk.CTkEntry(self.delete_frame, placeholder_text="Category ID")
        self.delete_id_entry.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(self.delete_frame, text="Delete", command=self.delete_category, 
                     fg_color="#FF5252", hover_color="#FF0000").pack(pady=10)
        
        # Categories Table
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        columns = ('ID', 'Name', 'Description', 'Product Count')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Refresh button
        ctk.CTkButton(self, text="Refresh Table", command=self.refresh_table).grid(row=2, column=1, pady=10)
        
        # Initial table load
        self.refresh_table()
    
    def create_category(self):
        try:
            name = self.name_entry.get()
            description = self.description_entry.get()
            
            if not name:
                messagebox.showerror("Error", "Category name is required")
                return
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO category (name, description)
                VALUES (?, ?)
            """, (name, description))
            
            conn.commit()
            conn.close()
            
            self.clear_create_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Category created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating category: {e}")
    
    def load_category(self):
        try:
            category_id = self.update_id_entry.get()
            if not category_id:
                messagebox.showerror("Error", "Please enter a category ID")
                return
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, description
                FROM category
                WHERE id = ?
            """, (int(category_id),))
            
            category = cursor.fetchone()
            conn.close()
            
            if category:
                self.update_name_entry.delete(0, 'end')
                self.update_name_entry.insert(0, category[0])
                self.update_description_entry.delete(0, 'end')
                self.update_description_entry.insert(0, category[1] or "")
            else:
                messagebox.showerror("Error", "Category not found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading category: {e}")
    
    def update_category(self):
        try:
            category_id = self.update_id_entry.get()
            new_name = self.update_name_entry.get()
            new_description = self.update_description_entry.get()
            
            if not category_id or not new_name:
                messagebox.showerror("Error", "Category ID and name are required")
                return
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE category
                SET name = ?, description = ?
                WHERE id = ?
            """, (new_name, new_description, int(category_id)))
            
            conn.commit()
            conn.close()
            
            self.clear_update_entries()
            self.refresh_table()
            messagebox.showinfo("Success", "Category updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating category: {e}")
    
    def delete_category(self):
        try:
            category_id = self.delete_id_entry.get()
            if not category_id:
                messagebox.showerror("Error", "Please enter a category ID")
                return
            
            # Check if category has products
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM products WHERE category_id = ?
            """, (int(category_id),))
            
            product_count = cursor.fetchone()[0]
            
            if product_count > 0:
                if not messagebox.askyesno("Warning", 
                    f"This category has {product_count} products. Deleting it will set their category to NULL. Continue?"):
                    conn.close()
                    return
            
            cursor.execute("""
                DELETE FROM category WHERE id = ?
            """, (int(category_id),))
            
            conn.commit()
            conn.close()
            
            self.delete_id_entry.delete(0, 'end')
            self.refresh_table()
            messagebox.showinfo("Success", "Category deleted successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting category: {e}")
    
    def refresh_table(self):
        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get categories with product count
            cursor.execute("""
                SELECT c.id, c.name, c.description,
                       COUNT(p.id) as product_count
                FROM category c
                LEFT JOIN products p ON c.id = p.category_id
                GROUP BY c.id
                ORDER BY c.name
            """)
            
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
                
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {e}")
    
    def clear_create_entries(self):
        self.name_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
    
    def clear_update_entries(self):
        self.update_id_entry.delete(0, 'end')
        self.update_name_entry.delete(0, 'end')
        self.update_description_entry.delete(0, 'end')
