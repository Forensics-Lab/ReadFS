import tkinter       as tk
import customtkinter as ctk
from PIL             import Image

class Quick_Open_Window(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.iconify()
        self.grab_set()

        self.window_width = 600
        self.window_height = 200

        x_offset = int((master.screen_width - self.window_width)   // 2 * master.scaleFactor)
        y_offset = int((master.screen_height - self.window_height) // 2 * master.scaleFactor)

        self.resizable(False, False)
        self.title("ReadFS - Quick Case")
        self.geometry(f"{self.window_width}x{self.window_height}+{x_offset}+{y_offset}")

        # VARIABLES
        self.radio_var = tk.IntVar()

        # IMAGES
        self.open_explorer_logo = ctk.CTkImage(Image.open("GUI/Graphics/assets/imgs/loupe.png"), size=(20, 20))

        # FRAMES
        self.frame = ctk.CTkFrame(self, width=self.window_width, height=self.window_height, corner_radius=0)

        # LABELS
        self.file_path_label = ctk.CTkLabel(self.frame, text="Evidence File Path", font=("GOST Common", 17))
        self.file_type_label = ctk.CTkLabel(self.frame, text="Evidence File Type", font=("GOST Common", 17))

        # ENTRIES
        self.entry = ctk.CTkEntry(self.frame, placeholder_text="/", font=("GOST Common", 17), width=310)

        # BUTTONS
        self.open_explorer_btn = ctk.CTkButton(self.frame, text='', image=self.open_explorer_logo,  command=self.open_explorer,       width=20, height=20)
        self.cancel_btn = ctk.CTkButton       (self.frame, text="Cancel", font=("GOST Common", 17), command=self.cancel_btn_callback, height=35)
        self.create_btn = ctk.CTkButton       (self.frame, text="Create", font=("GOST Common", 17), command=self.cancel_btn_callback, height=35)

        # RADIO BUTTONS
        self.logical_rbth  = ctk.CTkRadioButton(self.frame, text="Logical",  font=("GOST Common", 17), variable=self.radio_var, value=1)
        self.phisycal_rbtn = ctk.CTkRadioButton(self.frame, text="Physical", font=("GOST Common", 17), variable=self.radio_var, value=0)

        # PLACING
        self.file_path_label.place  (anchor="center", relx=0.18, rely=0.28)
        self.entry.place            (anchor="center", relx=0.58, rely=0.28)
        self.open_explorer_btn.place(anchor="center", relx=0.89, rely=0.28)

        self.file_type_label.place  (anchor="center", relx=0.18, rely=0.48)
        self.phisycal_rbtn.place    (anchor="center", relx=0.46, rely=0.48)
        self.logical_rbth.place     (anchor="center", relx=0.74, rely=0.48)

        self.create_btn.place       (anchor="center", relx=0.25, rely=0.80)
        self.cancel_btn.place       (anchor="center", relx=0.75, rely=0.80)

        self.frame.place(anchor="center", relx=0.5, rely=0.5)

    def cancel_btn_callback(self):
        self.destroy()
        self.master.deiconify()

    def open_explorer(self):
        filepath = ctk.filedialog.askopenfilename(initialdir="/")
        if filepath:
            self.entry.delete(0, "end")
            self.entry.insert(0, filepath)
