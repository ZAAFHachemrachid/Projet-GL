import customtkinter as ctk
from tkinter import messagebox
import sys
import os
print("Python path:", sys.path)
print("Current directory:", os.getcwd())
from PIL import Image

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_config import get_db_connection
from views.hardware_store import MainWindow

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("NANEF-Login")
        self.geometry("800x700")
        
        # Set theme background
        self.configure(fg_color="#ffffff")
        
        # Set close window protocol
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create background with pattern
        self.bg_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        self.bg_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Load and set background pattern
        bg_pattern_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                "static", "Login (3).png")
        try:
            bg_pattern = Image.open(bg_pattern_path)
            self.bg_pattern = ctk.CTkImage(
                light_image=bg_pattern,
                dark_image=bg_pattern,
                size=(800, 700)
            )
            self.bg_label = ctk.CTkLabel(self.bg_frame, image=self.bg_pattern, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Warning: Could not load background pattern: {e}")

        # Create main frame with glass effect
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#f0f0f0",
            corner_radius=30,
            width=400,
            height=600,
            border_width=0
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome text
        self.welcome_label = ctk.CTkLabel(
            self.main_frame,
            text="Welcome Back",
            font=("Arial Black", 24, "bold"),
            text_color="#000000"
        )
        self.welcome_label.place(relx=0.5, rely=0.12, anchor="center")

        # NANEF text
        self.nanef_label = ctk.CTkLabel(
            self.main_frame,
            text="NANEF",
            font=("Arial Black", 28, "bold"),
            text_color="#6c5ce7"
        )
        self.nanef_label.place(relx=0.5, rely=0.22, anchor="center")

        # Hardware Store text
        self.store_label = ctk.CTkLabel(
            self.main_frame,
            text="Hardware Store",
            font=("Arial", 14),
            text_color="#666666"
        )
        self.store_label.place(relx=0.5, rely=0.27, anchor="center")

        # Username label
        self.username_label = ctk.CTkLabel(
            self.main_frame,
            text="Username",
            font=("Arial Black", 14, "bold"),
            text_color="#000000"
        )
        self.username_label.place(relx=0.15, rely=0.4)

        # Username entry
        self.username_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            placeholder_text="Username",
            font=("Arial", 13),
            corner_radius=8,
            border_color="#E5E5E5",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#999999"
        )
        self.username_entry.place(relx=0.15, rely=0.45)

        # Password label
        self.password_label = ctk.CTkLabel(
            self.main_frame,
            text="Password",
            font=("Arial Black", 14, "bold"),
            text_color="#000000"
        )
        self.password_label.place(relx=0.15, rely=0.55)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            width=250,
            height=40,
            placeholder_text="••••••••••",
            font=("Arial", 13),
            corner_radius=8,
            border_color="#E5E5E5",
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text_color="#999999",
            show="•"
        )
        self.password_entry.place(relx=0.15, rely=0.6)

        # Remember me checkbox
        self.remember_var = ctk.BooleanVar()
        self.remember_checkbox = ctk.CTkCheckBox(
            self.main_frame,
            text="Remember me",
            variable=self.remember_var,
            font=("Arial", 12),
            text_color="#666666",
            fg_color="#6c5ce7",
            hover_color="#5f50e3",
            corner_radius=4
        )
        self.remember_checkbox.place(relx=0.3, rely=0.72)

        # Forgot password button
        self.forgot_button = ctk.CTkButton(
            self.main_frame,
            text="Forgot Password?",
            font=("Arial", 12),
            text_color="#6c5ce7",
            fg_color="transparent",
            hover_color="#f0f0f0",
            width=50,
            command=self.forgot_password_click
        )
        self.forgot_button.place(relx=0.7, rely=0.72)

        # Login button
        self.login_button = ctk.CTkButton(
            self.main_frame,
            width=220,
            height=45,
            text="Login",
            font=("Arial", 14, "bold"),
            corner_radius=8,
            fg_color="#6c5ce7",
            hover_color="#5f50e3",
            command=self.login
        )
        self.login_button.place(relx=0.5, rely=0.85, anchor="center")

        # Register text and button
        self.register_label = ctk.CTkLabel(
            self.main_frame,
            text="Don't have an account?",
            font=("Arial", 12),
            text_color="#666666"
        )
        self.register_label.place(relx=0.35, rely=0.92)

        self.register_button = ctk.CTkButton(
            self.main_frame,
            text="Register",
            font=("Arial", 12, "bold"),
            text_color="#6c5ce7",
            fg_color="transparent",
            hover_color="#f0f0f0",
            width=30,
            command=self.register_click
        )
        self.register_button.place(relx=0.7, rely=0.92)

    
        # Set initial focus
        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Please fill in all fields")
            return

        # Connect to database and verify credentials
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM users 
                WHERE username = ? AND password = ?
            """, (username, password))
            
            user = cursor.fetchone()
            if user:
                self.withdraw()  # Hide login window
                main_app = MainWindow(username)
                main_app.protocol("WM_DELETE_WINDOW", lambda: self.on_main_window_close(main_app))
                main_app.mainloop()
            else:
                messagebox.showerror("Error", "Invalid username or password")
                self.password_entry.delete(0, 'end')  # Clear password field
                self.password_entry.focus()  # Focus on password field
            
            conn.close()
                
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def forgot_password_click(self):
        self.destroy()
        from auth.forgot_password import ForgotPasswordWindow
        forgot_pwd = ForgotPasswordWindow()
        forgot_pwd.mainloop()

    def register_click(self):
        self.destroy()
        from auth.register import RegisterWindow
        register = RegisterWindow()
        register.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.quit()

    def on_main_window_close(self, main_window):
        main_window.destroy()
        self.destroy()  # Close the login window too

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
