import customtkinter as ctk
import sys
import os
from tkinter import messagebox

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_config import get_db_connection

# Import components
from views.components.sidebar import SidebarFrame
from views.components.product import ProductManagementFrame
from views.components.search_product import SearchProductFrame
from views.components.categories import CategoriesFrame
from views.components.stock_alert import StockAlertFrame
from views.components.checkout import CheckoutFrame

class ProfileDialog(ctk.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        
        self.title("User Profile")
        self.geometry("400x300")
        
        # Make the dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Center the dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
        
        # Profile content
        ctk.CTkLabel(
            self,
            text="Profile Information",
            font=("Arial", 24, "bold")
        ).pack(pady=20)
        
        # Username display
        username_frame = ctk.CTkFrame(self)
        username_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            username_frame,
            text="Username:",
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            username_frame,
            text=username,
            font=("Arial", 14)
        ).pack(side="left", padx=10)
        
        # Change password section
        password_frame = ctk.CTkFrame(self)
        password_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            password_frame,
            text="Change Password",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        self.current_password = ctk.CTkEntry(
            password_frame,
            placeholder_text="Current Password",
            show="*"
        )
        self.current_password.pack(pady=5, padx=10, fill="x")
        
        self.new_password = ctk.CTkEntry(
            password_frame,
            placeholder_text="New Password",
            show="*"
        )
        self.new_password.pack(pady=5, padx=10, fill="x")
        
        self.confirm_password = ctk.CTkEntry(
            password_frame,
            placeholder_text="Confirm New Password",
            show="*"
        )
        self.confirm_password.pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(
            password_frame,
            text="Change Password",
            command=self.change_password
        ).pack(pady=10)
    
    def change_password(self):
        current = self.current_password.get()
        new = self.new_password.get()
        confirm = self.confirm_password.get()
        
        if not all([current, new, confirm]):
            messagebox.showwarning("Warning", "All fields are required")
            return
        
        if new != confirm:
            messagebox.showwarning("Warning", "New passwords do not match")
            return
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verify current password
            cursor.execute("SELECT password FROM users WHERE username = ?", (self.master.username,))
            stored_password = cursor.fetchone()[0]
            
            if current != stored_password:  # In a real app, use proper password hashing
                messagebox.showerror("Error", "Current password is incorrect")
                return
            
            # Update password
            cursor.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (new, self.master.username)
            )
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Password changed successfully")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error changing password: {e}")

class MainWindow(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.conn = get_db_connection()

        # Configure window
        self.title("NANEF - Hardware Store")
        self.geometry("1200x700")
        self.configure(fg_color="#f0f0f0")

        # Create header
        self.create_header()
        
        # Create main content
        self.create_main_content()
        
        # Profile dialog reference
        self.profile_dialog = None

    def create_header(self):
        header = ctk.CTkFrame(self, height=50, fg_color="#6c5ce7")
        header.pack(fill="x", padx=0, pady=0)
        
        store_name = ctk.CTkLabel(
            header, 
            text="NANEF Hardware Store",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        store_name.pack(side="left", padx=20)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            header,
            text=f"Welcome, {self.username}",
            font=("Arial", 14),
            text_color="white"
        )
        welcome_label.pack(side="left", padx=20)
        
        logout_btn = ctk.CTkButton(
            header,
            text="Logout",
            fg_color="transparent",
            hover_color="#5b4cc7",
            text_color="white",
            height=30,
            command=self.logout
        )
        logout_btn.pack(side="right", padx=20)
        
        profile_btn = ctk.CTkButton(
            header,
            text="Profile",
            fg_color="transparent",
            hover_color="#5b4cc7",
            text_color="white",
            height=30,
            command=self.show_profile
        )
        profile_btn.pack(side="right", padx=20)

    def create_main_content(self):
        # Main content frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create and pack sidebar
        self.sidebar = SidebarFrame(self.main_frame, self.show_content)
        self.sidebar.pack(side="left", fill="y", padx=(0, 20))
        
        # Create content area
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        # Show initial content
        self.show_content("search_products")
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_content(self, content_type):
        self.clear_content()
        
        if content_type == "product":
            frame = ProductManagementFrame(self.content_frame)
        elif content_type == "search_products":
            frame = SearchProductFrame(self.content_frame)
        elif content_type == "categories":
            frame = CategoriesFrame(self.content_frame)
        elif content_type == "stock_alert":
            frame = StockAlertFrame(self.content_frame)
        elif content_type == "checkout":
            frame = CheckoutFrame(self.content_frame)
        
        frame.pack(fill="both", expand=True)
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.withdraw()  # Hide current window
            # Import here to avoid circular import
            from auth.login import LoginWindow
            login = LoginWindow()
            login.protocol("WM_DELETE_WINDOW", lambda: self.on_logout_close(login))
            login.mainloop()
    
    def on_logout_close(self, login_window):
        login_window.destroy()
        self.destroy()
    
    def show_profile(self):
        if self.profile_dialog is None or not self.profile_dialog.winfo_exists():
            self.profile_dialog = ProfileDialog(self, self.username)
        else:
            self.profile_dialog.focus()

if __name__ == "__main__":
    app = MainWindow("Admin")
    app.mainloop()
