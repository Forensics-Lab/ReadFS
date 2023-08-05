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
        self.case_manager       = case_manage
        self.dir_to_export      = path.abspath(f"data/cases/{dir_to_export}")
        self.default_dir        = StringVar(value = path.abspath("data/exports"))
        self.open_explorer_logo = ctk.CTkImage(Image.open("GUI/graphics/assets/imgs/loupe.png"), size=(20, 20))

        # LABELS
        self.ctk_label1 = ctk.CTkLabel(self, text=f"Output Directory", font=("GOST Common", 17))

        # ENTRIES
        self.ctk_entry1 = ctk.CTkEntry(self, textvariable=self.default_dir, width=319, font=("GOST Common", 17))

        # BUTTONS
        self.export_dir_button = ctk.CTkButton(self, text="", image=self.open_explorer_logo,  command=self.open_explorer,        width=30)
        self.export_btn        = ctk.CTkButton(self, text="Export", font=("GOST Common", 17), command=self.export_btn_callback, height=35)
        self.cancel_btn        = ctk.CTkButton(self, text="Cancel", font=("GOST Common", 17), command=self.cancel_btn_callback, height=35)

        # PLACING
        self.ctk_label1.place       (relx=0.17, rely=0.4, anchor="center")
        self.ctk_entry1.place       (relx=0.57, rely=0.4, anchor="center")
        self.export_dir_button.place(relx=0.9, rely=0.4, anchor="center" )

        self.export_btn.place(relx=0.2, rely=0.85, anchor="center")
        self.cancel_btn.place(relx=0.8, rely=0.85, anchor="center")


    def cancel_btn_callback(self):
        self.destroy()

    def export_btn_callback(self):
        self.case_manager.export(self.dir_to_export, self.ctk_entry1.get())
        if self.case_manager.status() == "SUCCESS":
            showinfo("ReadFS - Export", "Case has been exported successfully!")
            self.destroy()
        elif self.case_manager.status() == "EXPORT_PATH_NOT_SPECIFIED":
            showerror("ReadFS - Error", "Export path can not be empty!")
        elif self.case_manager.status() == "EXPORT_PATH_ALREADY_EXISTS":
            showerror("ReadFS - Error", "Case has already been exported to this path. Delete the old archive or choose another path!")
        self.case_manager.reset_status()

    def open_explorer(self):
        filepath = ctk.filedialog.askdirectory(initialdir=self.default_dir.get())
        if filepath:
            self.ctk_entry1.delete(0, "end")
            self.ctk_entry1.insert(0, filepath)
