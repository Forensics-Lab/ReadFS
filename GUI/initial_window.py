import ctypes
import customtkinter     as ctk
from GUI.new_case_window     import New_Case_Window
from GUI.quick_open_window   import Quick_Open_Window
from GUI.case_manager_window import Case_Manager_Window

class MenuWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        # Set the window's width and height
        self.app_width  = 900
        self.app_height = 500

        # Get the screen's width and height
        self.screen_height = self.winfo_screenheight()
        self.screen_width = self.winfo_screenwidth()

        # Set the window's title
        self.resizable(False, False)
        self.title("ReadFS - Menu")

        # Center the window
        self.x_offset = int((self.screen_height - self.app_height) // 2 * self.scaleFactor)
        self.y_offset = int((self.screen_width - self.app_width) // 2 * self.scaleFactor)
        self.geometry(f"{self.app_width}x{self.app_height}+{self.y_offset}+{self.x_offset}")

        # Label
        self.label = ctk.CTkLabel(self, justify="left", text="ReadFS", font=("GOST Common", 150))

        # Creating buttons
        self.new_case_bnt      = ctk.CTkButton(self, text="New Case",     width=300, height=70, font=("GOST Common", 25), command=lambda: New_Case_Window(self))
        self.quick_open_btn    = ctk.CTkButton(self, text="Quick Case",   width=300, height=70, font=("GOST Common", 25), command=lambda: Quick_Open_Window(self))
        self.continue_case_btn = ctk.CTkButton(self, text="Case Manager", width=300, height=70, font=("GOST Common", 25), command=lambda: Case_Manager_Window(self))

        self.label.place            (anchor="center", relx=0.5, rely=0.20)
        self.new_case_bnt.place     (anchor="center", relx=0.5, rely=0.50)
        self.quick_open_btn.place   (anchor="center", relx=0.5, rely=0.66)
        self.continue_case_btn.place(anchor="center", relx=0.5, rely=0.82)
