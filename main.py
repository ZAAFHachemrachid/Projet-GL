from database.db_config import setup_database
from auth.login import LoginWindow
import customtkinter as ctk
from views.hardware_store import MainWindow

if __name__ == "__main__":
    # Configure the appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Setup database
    setup_database()
    
    # Create and run the login window
    app = MainWindow("Admin")
    app.mainloop()