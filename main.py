import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json


class DynamicForm(ttk.Frame):
    def __init__(self, parent, form_items):
        super().__init__(parent)
        self.form_items = form_items
        self.entries = {}
        self.create_form()

    def create_form(self):
        for idx, (label_text, field_schema) in enumerate(self.form_items.items()):
            ttk.Label(self, text=label_text).grid(row=idx, column=0, padx=10, pady=10, sticky="w")
            if field_schema["type"] == "entry":
                entry = ttk.Entry(self)
                entry.grid(row=idx, column=1, padx=10, pady=10, sticky="w")
                self.entries[label_text] = entry
            if field_schema["type"] == "combobox":
                combobox = ttk.Combobox(self, values=field_schema["values"])
                combobox.grid(row=idx, column=1, padx=10, pady=10, sticky="w")
                self.entries[label_text] = combobox

            # Add more field types if needed

    def get_values(self):
        values = {}
        for label_text, entry in self.entries.items():
            values[label_text] = entry.get()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timesheet Management")
        self.geometry("1000x600")
        self.create_menu()
        self.create_nav()
        self.create_tabs()

    def create_menu(self):
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Settings", menu=file_menu)

        # Help menu
        employee_settings = tk.Menu(menubar, tearoff=0)
        employee_settings.add_command(label="Add Employee")
        employee_settings.add_command(label="View Employees")
        employee_settings.add_command(label="Delete Employee")
        menubar.add_cascade(label="Employee Settings", menu=employee_settings)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def create_nav(self):
        # Load an image file
        image = Image.open("mylogo.png")
        image = image.resize((200, 50), Image.LANCZOS)  # Adjust the size as needed

        # Create a new image with a white background
        background = Image.new("RGB", (200, 50), "white")
        background.paste(image, (0, 0), image)

        photo = ImageTk.PhotoImage(background)

        # Create a frame to hold the logo and buttons
        top_frame = ttk.Frame(self, style="TopFrame.TFrame")
        top_frame.pack(side="top", fill="x")

        # Create a style for the top frame
        style = ttk.Style()
        style.configure("TopFrame.TFrame", background="white")

        # Create a label to display the image
        logo_label = ttk.Label(top_frame, image=photo, background="white")
        logo_label.image = photo  # Keep a reference to avoid garbage collection
        logo_label.pack(side="left", anchor="nw")

        # Add a horizontal separator
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x", pady=3)

    def create_tabs(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.add_record_frame = ttk.Frame(self.notebook)
        self.view_records_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.add_record_frame, text="Add Record")
        self.notebook.add(self.view_records_frame, text="View Records")

        self.create_add_record_form()

        # Add content to the View Records tab
        ttk.Label(self.view_records_frame, text="View Records Content").pack(pady=20, padx=20)

    def create_add_record_form(self):
        data_error = False
        try:
            load_people = json.load(open("data.json"))["people"]
        except FileNotFoundError:
            load_people = []
        except json.JSONDecodeError:
            load_people = []
            data_error = True
        except KeyError:
            load_people = []

        if data_error:
            ttk.Label(self.add_record_frame, text="Something went wrong with people data").pack(pady=20, padx=20)
            return
        
        if not load_people:
            ttk.Label(self.add_record_frame, text="Add Employees to use the form").pack(pady=20, padx=20)
            return

        form_items = {
            "Name": {
                "type": "combobox",
                "values": load_people
            },
            "Date": {
                "type": "entry"
            },
            "Time": {
                "type": "entry"
            }
        }
        self.form = DynamicForm(self.add_record_frame, form_items)
        self.form.pack(pady=20, padx=20)

    def show_tab(self, index):
        self.notebook.select(index)

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()