import customtkinter            as ctk
from datetime                   import datetime
from tkinter.messagebox         import showerror
from GUI.Managers.Case          import Case_Manager
from GUI.Graphics.import_window import Import_Window
from GUI.Graphics.export_window import Export_Window
from tkinter                    import IntVar, StringVar


class Case_Manager_Window(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.iconify()
        self.grab_set()

        # Set the window's width and height
        self.window_width = 900
        self.window_height = 600

        # Get the screen's width and height
        x_offset = int((master.screen_width - self.window_width) // 2 * master.scaleFactor)
        y_offset = int((master.screen_height - self.window_height) // 2 * master.scaleFactor)

        # Set the window's title
        self.resizable(False, False)
        self.title("ReadFS - Case Manager")
        self.geometry(f"{self.window_width}x{self.window_height}+{x_offset}+{y_offset}")

        # VARIABLES
        self.radio_btn_id     = 0
        self.entries          = {}
        self.case_directories = {}
        self.case_manager     = Case_Manager()
        self.radio_var        = IntVar(value=0)
        self.entry_row_pos    = len(self.entries)

        # FRAMES
        self.master_frame = ctk.CTkFrame(self, width=self.window_width, height=self.window_height, corner_radius=0)
        self.scroll_frame = ctk.CTkFrame(self.master_frame, width=self.window_width//1.2, height=self.window_height//1.3, corner_radius=0,fg_color="transparent")

        # SCROLLABLE FRAME
        self.scroll_window = ctk.CTkScrollableFrame(self.scroll_frame, width=self.window_width//1.2, height=self.window_height//1.3, corner_radius=0,
                                                    scrollbar_fg_color="transparent",
                                                    scrollbar_button_color="",
                                                    scrollbar_button_hover_color="",
                                                    fg_color="transparent")
        # LABELS
        self.ctk_label1 = ctk.CTkLabel(self.master_frame, text=f"Case No.",      font=("GOST Common", 20))
        self.ctk_label2 = ctk.CTkLabel(self.master_frame, text=f"Examiner",      font=("GOST Common", 20))
        self.ctk_label3 = ctk.CTkLabel(self.master_frame, text=f"Created",       font=("GOST Common", 20))
        self.ctk_label4 = ctk.CTkLabel(self.master_frame, text=f"Last Modified", font=("GOST Common", 20))

        # BUTTONS
        self.open_btn   = ctk.CTkButton(self.master_frame, text="Open",   font=("GOST Common", 17), command=self.cancel_btn_callback, height=35)
        self.import_btn = ctk.CTkButton(self.master_frame, text="Import", font=("GOST Common", 17), command=self.import_btn_callback, height=35)
        self.export_btn = ctk.CTkButton(self.master_frame, text="Export", font=("GOST Common", 17), command=self.export_btn_callback, height=35)
        self.delete_btn = ctk.CTkButton(self.master_frame, text="Delete", font=("GOST Common", 17), command=self.delete_btn_callback, height=35)
        self.cancel_btn = ctk.CTkButton(self.master_frame, text="Cancel", font=("GOST Common", 17), command=self.cancel_btn_callback, height=35)

        # ADDING ENTRIES
        cases = self.get_cases()
        if cases:
            for case in cases:
                date_created = datetime.fromtimestamp(case['date_created']).strftime("%d/%m/%Y")
                date_modified = datetime.fromtimestamp(case['date_modified']).strftime("%d/%m/%Y")
                self.add_entry(case["case_id"], case["case_no"], case['author'].replace('_', ' '), date_created, date_modified)

        # PLACING
        self.open_btn.place  (anchor="center", relx=0.150, rely=0.94)
        self.import_btn.place(anchor="center", relx=0.325, rely=0.94)
        self.export_btn.place(anchor="center", relx=0.500, rely=0.94)
        self.delete_btn.place(anchor="center", relx=0.675, rely=0.94)
        self.cancel_btn.place(anchor="center", relx=0.850, rely=0.94)

        self.master_frame.place(anchor="center", relx=0.5, rely=0.5)
        self.scroll_frame.place(anchor="center", relx=0.5, rely=0.5)

        self.ctk_label1.place(anchor="center", relx=0.220, rely=0.05)
        self.ctk_label2.place(anchor="center", relx=0.420, rely=0.05)
        self.ctk_label3.place(anchor="center", relx=0.615, rely=0.05)
        self.ctk_label4.place(anchor="center", relx=0.820, rely=0.05)

        self.scroll_window.place(anchor="center", relx=0.51, rely=0.5)

    def add_entry(self, entry_id, case_no, author, created, last_modified):
        rbtn = ctk.CTkRadioButton(self.scroll_window, text='', bg_color='transparent', width=1, height=1, value=self.radio_btn_id, variable=self.radio_var)
        f1 =   ctk.CTkFrame   (self.scroll_window, width=self.window_width // 5, height=50, corner_radius=0, border_width=1)
        f2 =   ctk.CTkFrame   (self.scroll_window, width=self.window_width // 5, height=50, corner_radius=0, border_width=1)
        f3 =   ctk.CTkFrame   (self.scroll_window, width=self.window_width // 5, height=50, corner_radius=0, border_width=1)
        f4 =   ctk.CTkFrame   (self.scroll_window, width=self.window_width // 5, height=50, corner_radius=0, border_width=1)

        ctk.CTkLabel(f1, text=self.trim_entry(case_no), font=("GOST Common", 16)).place(anchor="center", relx=0.5, rely=0.5)
        ctk.CTkLabel(f2, text=self.trim_entry(author),  font=("GOST Common", 16)).place(anchor="center", relx=0.5, rely=0.5)
        ctk.CTkLabel(f3, text=created,                  font=("GOST Common", 16)).place(anchor="center", relx=0.5, rely=0.5)
        ctk.CTkLabel(f4, text=last_modified,            font=("GOST Common", 16)).place(anchor="center", relx=0.5, rely=0.5)

        rbtn.grid(row=self.entry_row_pos, column=0)
        f1.grid  (row=self.entry_row_pos, column=1)
        f2.grid  (row=self.entry_row_pos, column=2)
        f3.grid  (row=self.entry_row_pos, column=3)
        f4.grid  (row=self.entry_row_pos, column=4)
        self.case_directories[self.radio_btn_id] = StringVar(value=entry_id)
        self.entries[self.radio_btn_id] = [rbtn, f1, f2, f3, f4]
        self.entry_row_pos += 1
        self.radio_btn_id += 1

    def trim_entry(self, entry, max_len=15):
        return entry[:max_len] + "..." if len(entry) > max_len else entry

    def cancel_btn_callback(self):
        self.destroy()
        self.master.deiconify()

    def import_btn_callback(self):
        tmp = Import_Window(self.master, self, self.case_manager)
        tmp.mainloop()

    def export_btn_callback(self):
        # This section may change in the future
        if self.entries:
            entry_key = self.radio_var.get()
            tmp = Export_Window(self.master, self.case_manager, self.case_directories[entry_key].get())
            tmp.mainloop()
        elif not self.entries:
            showerror("ReadFS - Error", "No cases to export")

    def delete_btn_callback(self):
        if not self.entries:           showerror("ReadFS - Error", "No case to delete."); return
        if self.radio_var.get() == -1: showerror("ReadFS - Error", "No case selected." ); return
        # Delete the widget from the screen
        entry_key = self.radio_var.get()
        for widget in self.entries[entry_key]:
            widget.destroy()
        # Delete the entry from the entries dictionary
        self.entries.pop(entry_key)
        self.update_rows(self.entries)
        self.radio_var.set(-1)
        self.entry_row_pos -= 1
        self.radio_btn_id += 1

        # Delete the case from disk
        self.case_manager.delete(self.case_directories[entry_key].get())
        self.case_directories.pop(entry_key)

    def update_rows(self, entries):
        for row, entry in enumerate(entries.items()):
            for col, widget in enumerate(entry[1]):
                widget.grid_forget()
                widget.grid(row=row, column=col)

    def get_cases(self):
        cases_data = []
        cases_dirs = self.case_manager.list()
        for case in cases_dirs:
            case_data = self.case_manager.get_case_metadata(case)
            cases_data.append(case_data)
        return cases_data