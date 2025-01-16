import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import Calendar
import json
import datetime
import csv
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk


def open_time_picker(parent, callback):
    def select_time():
        selected_hour = hour_spinbox.get()
        selected_minute = minute_spinbox.get()
        selected_period = period_combobox.get()
        time_str = f"{selected_hour}:{selected_minute} {selected_period}"
        callback(time_str)
        time_window.destroy()

    time_window = tk.Toplevel(parent)
    time_window.title("Select Time")
    time_window.geometry("250x150")

    # Hour selection
    ttk.Label(time_window, text="Hour:").grid(row=0, column=0, padx=10, pady=10)
    hour_spinbox = ttk.Spinbox(time_window, from_=1, to=12, width=5, wrap=True)
    hour_spinbox.grid(row=0, column=1, padx=10, pady=10)

    # Minute selection
    ttk.Label(time_window, text="Minute:").grid(row=1, column=0, padx=10, pady=10)
    minute_spinbox = ttk.Spinbox(time_window, from_=0, to=59, width=5, wrap=True, format="%02.0f")
    minute_spinbox.grid(row=1, column=1, padx=10, pady=10)

    # AM/PM selection
    ttk.Label(time_window, text="Period:").grid(row=2, column=0, padx=10, pady=10)
    period_combobox = ttk.Combobox(time_window, values=["AM", "PM"], state="readonly", width=5)
    period_combobox.set("AM")
    period_combobox.grid(row=2, column=1, padx=10, pady=10)

    # Confirm button
    ttk.Button(time_window, text="Select", command=select_time).grid(row=3, column=0, columnspan=2, pady=10)
def open_calendar(parent, callback):
    def select_date():
        selected_date = calendar.get_date()
        callback(selected_date)
        calendar_window.destroy()

    calendar_window = tk.Toplevel(parent)
    calendar_window.title("Select Date")
    calendar_window.geometry("300x300")

    # Add a Calendar widget
    calendar = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
    calendar.pack(pady=20)

    # Add a button to confirm date selection
    ttk.Button(calendar_window, text="Select Date", command=select_date).pack(pady=10)




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
            
            elif field_schema["type"] == "combobox":
                combobox = ttk.Combobox(self, values=field_schema["values"], state="readonly")
                combobox.grid(row=idx, column=1, padx=10, pady=10, sticky="w")
                self.entries[label_text] = combobox
            
            elif field_schema["type"] == "calender":
                date_var = tk.StringVar()
                ttk.Entry(self, textvariable=date_var, state="readonly").grid(row=idx, column=1, padx=10, pady=10, sticky="w")

                # Ensure the callback for the calendar is unique
                def pick_date(var=date_var):
                    open_calendar(self, lambda date_str: var.set(date_str))

                ttk.Button(self, text="Pick Date", command=pick_date).grid(row=idx, column=2, padx=10, pady=10, sticky="w")

                self.entries[label_text] = date_var



            elif field_schema["type"] == "time":
                time_var = tk.StringVar()
                ttk.Entry(self, textvariable=time_var, state="readonly").grid(row=idx, column=1, padx=10, pady=10, sticky="w")

                # Ensure the callback for each time picker is unique
                def pick_time(var=time_var):
                    open_time_picker(self, lambda time_str: var.set(time_str))

                ttk.Button(self, text="Pick Time", command=pick_time).grid(row=idx, column=2, padx=10, pady=10, sticky="w")

                self.entries[label_text] = time_var


    def get_values(self):
        values = {}
        for label_text, entry in self.entries.items():
            values[label_text] = entry.get()
        return values


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

        # Employee Settings menu
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
        try:
            # Load an image file
            image = Image.open("mylogo.png")
            image = image.resize((200, 50), Image.LANCZOS)

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

        except FileNotFoundError:
            print("Logo file not found.")

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

        # Add a tab change event to load records dynamically
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "View Records":
            self.create_view_records_table()


    def create_add_record_form(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                load_people = data.get("people", [])
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            load_people = []

        if not load_people:
            ttk.Label(self.add_record_frame, text="Add Employees to use the form").pack(pady=20, padx=20)
            return

        form_items = {
            "Term": {"type": "entry"},
            "Week": {"type": "entry"},
            "Date": {"type": "calender"},
            "Name": {"type": "combobox", "values": load_people},
            "In Time": {"type": "time"},
            "Out Time": {"type": "time"},
            "Break": {"type": "entry"}
        }
        self.form = DynamicForm(self.add_record_frame, form_items)
        self.form.pack(pady=20, padx=20)

        # Create Save and Clear buttons in a single row
        button_frame = ttk.Frame(self.add_record_frame)
        button_frame.pack(pady=10)

        save_button = ttk.Button(button_frame, text="Save", command=self.save_record)
        save_button.grid(row=0, column=0, padx=10)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_form)
        clear_button.grid(row=0, column=1, padx=10)

  

    def create_view_records_table(self):
            # Clear previous table content (if any)
            for widget in self.view_records_frame.winfo_children():
                widget.destroy()

            # Read data from CSV file and populate the table
            try:
                with open("records.csv", "r", newline="") as file:
                    reader = csv.DictReader(file)
                    rows = list(reader)

                if rows:
                    columns = list(rows[0].keys())  # Get column names from the first row
                else:
                    columns = []

                # Create Treeview widget to display data
                table = ttk.Treeview(self.view_records_frame, columns=columns, show="headings")
                table.pack(fill="both", expand=True)

                # Add columns to the table
                for col in columns:
                    table.heading(col, text=col)
                    table.column(col, width=100)

                # Insert rows into the table
                for row in rows:
                    table.insert("", "end", values=[row[col] for col in columns])

            except FileNotFoundError:
                ttk.Label(self.view_records_frame, text="No records found.").pack(pady=20, padx=20)
    
    def create_view_records_table(self):
        # Clear previous table content (if any)
        for widget in self.view_records_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.view_records_frame, text="Timesheet Records", font=("Arial", 16)).pack(pady=10)

        try:
            with open("timesheet_records.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            if rows:
                columns = list(rows[0].keys())  # Get column names from the first row
            else:
                columns = []

            if not columns:
                ttk.Label(self.view_records_frame, text="No records found in the file.").pack(pady=20)
                return

            # Create Treeview widget to display data
            table_frame = ttk.Frame(self.view_records_frame)
            table_frame.pack(fill="both", expand=True)

            table = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
            table.pack(side="left", fill="both", expand=True)

            # Add vertical scrollbar
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
            table.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Add columns to the table
            for col in columns:
                table.heading(col, text=col, anchor="center")  # Center-align headers
                table.column(col, anchor="center", width=100)  # Center-align data

            # Insert rows into the table
            for row in rows:
                table.insert("", "end", values=[row[col] for col in columns])

        except FileNotFoundError:
            ttk.Label(self.view_records_frame, text="No records file found.").pack(pady=20)




    def save_record(self):
        values = self.form.get_values()

        # Validate all fields are filled
        for key, value in values.items():
            if not value.strip():
                messagebox.showerror("Incomplete Form", f"Please fill in the '{key}' field.")
                return

        # Extract values
        term = values.get("Term")
        week = values.get("Week")
        date = values.get("Date")
        name = values.get("Name")
        in_time = values.get("In Time")
        out_time = values.get("Out Time")
        break_time = values.get("Break")

        # Validate times
        try:
            in_time_obj = datetime.datetime.strptime(in_time, "%I:%M %p").time()
            out_time_obj = datetime.datetime.strptime(out_time, "%I:%M %p").time()
        except ValueError:
            messagebox.showerror("Invalid Time", "Please ensure both times are correctly selected.")
            return

        if in_time_obj >= out_time_obj:
            messagebox.showerror("Invalid Time Range", "In Time must be earlier than Out Time.")
            return

        # Save to CSV
        try:
            with open("timesheet_records.csv", "a", newline="") as file:
                writer = csv.writer(file)

                # Write headers if the file is empty
                if file.tell() == 0:
                    writer.writerow(["Term", "Week", "Date", "Name", "In Time", "Out Time", "Break"])

                writer.writerow([term, week, date, name, in_time, out_time, break_time])

            messagebox.showinfo("Success", "Data recorded successfully!")

            # Clear form fields
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the record: {e}")




    def clear_form(self):
        # Assuming `self.form.entries` holds all the form fields (Entry widgets, etc.)
        for entry in self.form.entries.values():
            if isinstance(entry, tk.StringVar):
                entry.set("")  # Clear StringVar-based fields (e.g., calendar and time)
            elif isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)  # Clear Entry and Combobox fields






def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
