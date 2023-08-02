from PIL import Image
import tkinter       as tk
import customtkinter as ctk

class New_Case_Window(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.iconify()
        self.grab_set()

        self.window_width  = 600
        self.window_height = 300

        x_offset = int((master.screen_width  - self.window_width)  // 2 * master.scaleFactor)
        y_offset = int((master.screen_height - self.window_height) // 2 * master.scaleFactor)

        self.resizable(False, False)
        self.title    ("ReadFS - New Case")
        self.geometry (f"{self.window_width}x{self.window_height}+{x_offset}+{y_offset}")

        self.frame = ctk.CTkFrame(self, width=self.window_width, height=self.window_height, corner_radius=0)

        self.open_explorer_logo = ctk.CTkImage(Image.open("GUI/assets/imgs/loupe.png"), size=(20, 20))

        # VARIABLES
        self.radio_var = tk.IntVar(value=0)

        # LABELS
        self.case_no_label        = ctk.CTkLabel(self.frame, text="Case No.",      font=("GOST Common", 17))
        self.case_author_label    = ctk.CTkLabel(self.frame, text="Examiner",      font=("GOST Common", 17))
        self.case_imagefile_label = ctk.CTkLabel(self.frame, text="Evidence File", font=("GOST Common", 17))
        self.imagefile_type       = ctk.CTkLabel(self.frame, text="Image Type",    font=("GOST Common", 17))

        # ENTRIES
        self.case_no_entry         = ctk.CTkEntry(self.frame, placeholder_text="001",      font=("GOST Common", 17), width=317)
        self.case_author_entry     = ctk.CTkEntry(self.frame, placeholder_text="John Doe", font=("GOST Common", 17), width=317)
        self.case_image_file_entry = ctk.CTkEntry(self.frame, placeholder_text="/",        font=("GOST Common", 17), width=276)

        # BUTTONS
        self.case_imagefile_button = ctk.CTkButton(self.frame, text="", image=self.open_explorer_logo,  command=self.open_explorer,           width=30)
        self.create_button         = ctk.CTkButton(self.frame, text="Create", font=("GOST Common", 17), command=self.create_case,            height=35)
        self.cancel_button         = ctk.CTkButton(self.frame, text="Cancel", font=("GOST Common", 17), command=self.cancel_button_callback, height=35)

        # RADIO BUTTONS
        self.radio_button_1 = ctk.CTkRadioButton(self.frame, text="Logical",  variable=self.radio_var, value=1)
        self.radio_button_2 = ctk.CTkRadioButton(self.frame, text="Physical", variable=self.radio_var, value=0)

        # PLACING
        self.case_no_label.place       (anchor="w", relx=0.10, rely=0.20)
        self.case_author_label.place   (anchor="w", relx=0.10, rely=0.35)
        self.case_imagefile_label.place(anchor="w", relx=0.10, rely=0.50)
        self.imagefile_type.place      (anchor="w", relx=0.10, rely=0.65)

        self.case_no_entry.place        (anchor="w", relx=0.35, rely=0.20)
        self.case_author_entry.place    (anchor="w", relx=0.35, rely=0.35)
        self.case_image_file_entry.place(anchor="w", relx=0.35, rely=0.50)

        self.case_imagefile_button.place(anchor="w",      relx=0.82, rely=0.50)
        self.create_button.place        (anchor="center", relx=0.25, rely=0.85)
        self.cancel_button.place        (anchor="center", relx=0.75, rely=0.85)

        self.radio_button_1.place(anchor="w", relx=0.67, rely=0.65)
        self.radio_button_2.place(anchor="w", relx=0.40, rely=0.65)

        self.frame.place(anchor="center", relx=0.5, rely=0.5)

    def create_case(self):
        if self.case_image_file_entry.get() == "":
            tk.messagebox.showerror("ReadFS - Error", "To create a case you must select an image file.")
            return
        tk.messagebox.showinfo("ReadFS - Success", "Case created successfully.")
        self.destroy()
        self.master.deiconify()

    def cancel_button_callback(self):
        self.destroy()
        self.master.deiconify()

    def open_explorer(self):
        filepath = ctk.filedialog.askopenfilename(initialdir="/")
        if filepath:
            self.case_image_file_entry.delete(0, "end")
            self.case_image_file_entry.insert(0, filepath)