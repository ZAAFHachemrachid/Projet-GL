import customtkinter as ctk

class AddProductFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        title = ctk.CTkLabel(
            self,
            text="Add New Product",
            font=("Arial", 24, "bold"),
            text_color="#333333"
        )
        title.pack(pady=20)
        
        # TODO: Add product form
