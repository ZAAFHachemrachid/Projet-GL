import customtkinter as ctk

class CategoriesFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        title = ctk.CTkLabel(
            self,
            text="Categories",
            font=("Arial", 24, "bold"),
            text_color="#333333"
        )
        title.pack(pady=20)
        
        # TODO: Implement categories view
