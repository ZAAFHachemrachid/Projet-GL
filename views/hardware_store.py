import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_config import get_db_connection

# Import components
from views.components.sidebar import SidebarFrame
from views.components.add_product import AddProductFrame
from views.components.search_product import SearchProductFrame
from views.components.categories import CategoriesFrame
from views.components.stock_alert import StockAlertFrame
from views.components.checkout import CheckoutFrame

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
        
        logout_btn = ctk.CTkButton(
            header,
            text="Logout",
            fg_color="transparent",
            hover_color="#5b4cc7",
            text_color="white",
            height=30
        )
        logout_btn.pack(side="right", padx=20)
        
        profile_btn = ctk.CTkButton(
            header,
            text="Profile",
            fg_color="transparent",
            hover_color="#5b4cc7",
            text_color="white",
            height=30
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
        
        if content_type == "add_product":
            frame = AddProductFrame(self.content_frame)
        elif content_type == "search_products":
            frame = SearchProductFrame(self.content_frame)
        elif content_type == "categories":
            frame = CategoriesFrame(self.content_frame)
        elif content_type == "stock_alert":
            frame = StockAlertFrame(self.content_frame)
        elif content_type == "checkout":
            frame = CheckoutFrame(self.content_frame)
        
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainWindow("Admin")
    app.mainloop()
