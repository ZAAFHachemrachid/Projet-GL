import customtkinter as ctk

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, parent, show_content_callback, **kwargs):
        super().__init__(parent, fg_color="transparent", width=200, **kwargs)
        self.show_content_callback = show_content_callback
        
        # Menu label
        menu_label = ctk.CTkLabel(
            self,
            text="Menu",
            font=("Arial", 16, "bold"),
            text_color="#333333"
        )
        menu_label.pack(anchor="w", pady=(0, 10))
        
        # Menu buttons
        menu_items = [
            ("📦 Product", self.show_product),
            ("🔍 Search Products", self.show_search_products),
            ("📁 Categories", self.show_categories),
            ("⚠️ Stock Alert", self.show_stock_alert),
            ("📊 Check  ", self.show_checkout)
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                self,
                text=text,
                fg_color="transparent",
                text_color="#333333",
                hover_color="#e0e0e0",
                anchor="w",
                height=35,
                command=command
            )
            btn.pack(fill="x", pady=2)
    
    def show_product(self):
        self.show_content_callback("product")
    
    def show_search_products(self):
        self.show_content_callback("search_products")
    
    def show_categories(self):
        self.show_content_callback("categories")
    
    def show_stock_alert(self):
        self.show_content_callback("stock_alert")
    
    def show_checkout(self):
        self.show_content_callback("checkout")
