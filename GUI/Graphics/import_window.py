import customtkinter    as ctk
from PIL                import Image
from datetime           import datetime
from tkinter            import StringVar
from os                 import path, getcwd
from tkinter.messagebox import showerror, showinfo


class Import_Window(ctk.CTkToplevel):
    def __init__(self, master, slave, case_manage):
        super().__init__(master)
        self.slave = slave
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
        self.title("ReadFS - Import")
        self.geometry(f"{self.window_width}x{self.window_height}+{x_offset}+{y_offset}")

        # VARIABLES
        self.case_manager        = case_manage
        self.password            = StringVar(value="ReadFS")
        self.default_import_path = StringVar(value=path.abspath(getcwd()))
        self.open_explorer_logo  = ctk.CTkImage(Image.open("GUI/Graphics/assets/imgs/loupe.png"), size=(20, 20))

        # LABELS
        self.ctk_label1 = ctk.CTkLabel(self, text=f"Output Directory", font=("GOST Common", 17))
        self.ctk_label2 = ctk.CTkLabel(self, text=f"Password",         font=("GOST Common", 17))

        # ENTRIES
        self.path_to_zip = ctk.CTkEntry(self, textvariable=self.default_import_path, width=319, font=("GOST Common", 17))
        self.password    = ctk.CTkEntry(self, textvariable=self.password, show="*",  width=319, font=("GOST Common", 17))

        # BUTTONS
        self.import_dir_button = ctk.CTkButton(self, text="", image=self.open_explorer_logo,  command=self.open_explorer,        width=30)
        self.import_btn        = ctk.CTkButton(self, text="Import", font=("GOST Common", 17), command=self.import_btn_callback, height=35)
        self.cancel_btn        = ctk.CTkButton(self, text="Cancel", font=("GOST Common", 17), command=self.cancel_btn_callback, height=35)

        # PLACING
        self.ctk_label1.place       (relx=0.17, rely=0.28, anchor="center")
        self.path_to_zip.place      (relx=0.57, rely=0.28, anchor="center")
        self.import_dir_button.place(relx=0.90, rely=0.28, anchor="center")

        self.ctk_label2.place(relx=0.129, rely=0.53, anchor="center")
        self.password.place  (relx=0.570, rely=0.53, anchor="center")

        self.import_btn.place(relx=0.2, rely=0.85, anchor="center")
        self.cancel_btn.place(relx=0.8, rely=0.85, anchor="center")

    def cancel_btn_callback(self):
        self.destroy()

    def import_btn_callback(self):
        self.case_manager.import_(self.path_to_zip.get(), self.password.get())
        if self.case_manager.status() == "SUCCESS":
            showinfo("ReadFS - Import", "Case has been imported successfully!")
            case = self.slave.get_cases()[-1]
            date_created = datetime.fromtimestamp(case['date_created']).strftime("%d/%m/%Y")
            date_modified = datetime.fromtimestamp(case['date_modified']).strftime("%d/%m/%Y")
            self.slave.add_entry(case["case_id"], case["case_no"], case['author'].replace('_', ' '), date_created,date_modified)
            self.destroy()
        elif self.case_manager.status() == "EMPTY_IMPORT_PATH":
            showerror("ReadFS - Import", "Path cannot be empty!")
        elif self.case_manager.status() == "BAD_IMPORT_FILE":
            showerror("ReadFS - Import", "File is not a valid ReadFS case!")
        elif self.case_manager.status() == "IMPORT_FILE_NOT_FOUND":
            showerror("ReadFS - Import", "Invalid path!")
        elif self.case_manager.status() == "INVALID_PASSWORD":
            showerror("ReadFS - Import", "Invalid password!")
        self.case_manager.reset_status()

    def open_explorer(self):
        filepath = ctk.filedialog.askopenfilename(defaultextension="zip", initialdir=self.default_import_path.get())
        if filepath:
            self.path_to_zip.delete(0, "end")
            self.path_to_zip.insert(0, filepath)