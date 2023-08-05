import customtkinter    as ctk
from os                 import path
from PIL                import Image
from tkinter            import StringVar
from tkinter.messagebox import showerror, showinfo


class Export_Window(ctk.CTkToplevel):
    def __init__(self, master, case_manage, dir_to_export):
        super().__init__(master)
        self.master = master
        self.master.iconify()
        self.grab_set()

        # Set the window's width and height
        self.window_width = 600
        self.window_height = 200

        # Get the screen's width and height
        x_offset = int((master.screen_width - self.window_width) // 2 * master.scaleFactor)
        y_offset = int((master.screen_height - self.window_height) // 2 * master.scaleFactor)

        # Set the window's title
        self.resizable(False, False)
        self.title("ReadFS - Export")
        self.geometry(f"{self.window_width}x{self.window_height}+{x_offset}+{y_offset}")

        # VARIABLES
        self.password           = StringVar(value="ReadFS")
        self.case_manager       = case_manage
        self.dir_to_export      = path.abspath(f"data/cases/{dir_to_export}")
        self.default_dir        = StringVar(value = path.abspath("data/exports"))
        self.open_explorer_logo = ctk.CTkImage(Image.open("GUI/Graphics/assets/imgs/loupe.png"), size=(20, 20))

        # LABELS
        self.ctk_label1 = ctk.CTkLabel(self, text=f"Output Directory", font=("GOST Common", 17))
        self.ctk_label2 = ctk.CTkLabel(self, text=f"Password",         font=("GOST Common", 17))

        # ENTRIES
        self.export_path = ctk.CTkEntry(self, textvariable=self.default_dir,        width=319, font=("GOST Common", 17))
        self.password    = ctk.CTkEntry(self, textvariable=self.password, show="*", width=319, font=("GOST Common", 17))

        # BUTTONS
        self.export_dir_button = ctk.CTkButton(self, text="", image=self.open_explorer_logo,  command=self.open_explorer,        width=30)
        self.export_btn        = ctk.CTkButton(self, text="Export", font=("GOST Common", 17), command=self.export_btn_callback, height=35)
        self.cancel_btn        = ctk.CTkButton(self, text="Cancel", font=("GOST Common", 17), command=self.cancel_btn_callback, height=35)

        # PLACING
        self.ctk_label1.place       (relx=0.17, rely=0.28, anchor="center")
        self.export_path.place      (relx=0.57, rely=0.28, anchor="center")
        self.export_dir_button.place(relx=0.90, rely=0.28, anchor="center")

        self.ctk_label2.place(relx=0.129, rely=0.53, anchor="center")
        self.password.place  (relx=0.570, rely=0.53, anchor="center")

        self.export_btn.place(relx=0.2, rely=0.85, anchor="center")
        self.cancel_btn.place(relx=0.8, rely=0.85, anchor="center")

    def cancel_btn_callback(self):
        self.destroy()

    def export_btn_callback(self):
        self.case_manager.export(self.dir_to_export, self.export_path.get(), self.password.get())
        if self.case_manager.status() == "SUCCESS":
            showinfo("ReadFS - Export", "Case has been exported successfully!")
            self.destroy()
        elif self.case_manager.status() == "INVALID_EXPORT_PATH":
            showerror("ReadFS - Error", "Invalid export path!")
        elif self.case_manager.status() == "EMPTY_EXPORT_PATH":
            showerror("ReadFS - Error", "Export path cannot be empty!")
        elif self.case_manager.status() == "PASSWORD_NOT_PROVIDED":
            showerror("ReadFS - Error", "Password cannot be empty!")
        self.case_manager.reset_status()

    def open_explorer(self):
        filepath = ctk.filedialog.askdirectory(initialdir=self.default_dir.get())
        if filepath:
            self.export_path.delete(0, "end")
            self.export_path.insert(0, filepath)
