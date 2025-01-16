import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import Calendar
import json
import datetime
import csv
from tkinter import messagebox


class TimePicker:
    @staticmethod
    def open(parent, callback):
        def select_time():
            selected_hour = hour_spinbox.get()
            selected_minute = minute_spinbox.get()
            selected_period = period_combobox.get()
            time_str = f"{selected_hour}:{selected_minute} {selected_period}"
            callback(time_str)
            time_window.destroy()

        time_window = tk.Toplevel(parent)
        time_window.title("Select Time")
        time_window.geometry("250x250")

        ttk.Label(time_window, text="Hour:").grid(row=0, column=0, padx=10, pady=10)
        hour_spinbox = ttk.Spinbox(time_window, from_=1, to=12, width=5, wrap=True)
        hour_spinbox.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(time_window, text="Minute:").grid(row=1, column=0, padx=10, pady=10)
        minute_spinbox = ttk.Spinbox(time_window, from_=0, to=59, width=5, wrap=True, format="%02.0f")
        minute_spinbox.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(time_window, text="Period:").grid(row=2, column=0, padx=10, pady=10)
        period_combobox = ttk.Combobox(time_window, values=["AM", "PM"], state="readonly", width=5)
        period_combobox.set("AM")
        period_combobox.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(time_window, text="Select", command=select_time).grid(row=3, column=0, columnspan=2, pady=10)


class CalendarPicker:
    @staticmethod
    def open(parent, callback):
        def select_date():
            selected_date = calendar.get_date()
            callback(selected_date)
            calendar_window.destroy()

        calendar_window = tk.Toplevel(parent)
        calendar_window.title("Select Date")
        calendar_window.geometry("300x300")

        calendar = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
        calendar.pack(pady=20)

        ttk.Button(calendar_window, text="Select Date", command=select_date).pack(pady=10)

class DynamicForm(ttk.Frame):
    def __init__(self, parent, form_items):
        super().__init__(parent)
        self.form_items = form_items
        self.entries = {}
        self.create_form()

    def create_form(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))

        for idx, (label_text, field_schema) in enumerate(self.form_items.items()):
            ttk.Label(self, text=label_text, style="TLabel").grid(row=idx, column=0, padx=10, pady=10, sticky="w")

            if field_schema["type"] == "entry":
                entry = ttk.Entry(self, style="TEntry")
                entry.grid(row=idx, column=1, padx=10, pady=10, sticky="w")
                self.entries[label_text] = entry

            elif field_schema["type"] == "combobox":
                combobox = ttk.Combobox(self, values=field_schema["values"], state="readonly", style="TCombobox")
                combobox.grid(row=idx, column=1, padx=10, pady=10, sticky="w")
                self.entries[label_text] = combobox

            elif field_schema["type"] == "calendar":
                date_var = tk.StringVar()
                ttk.Entry(self, textvariable=date_var, state="readonly", style="TEntry").grid(row=idx, column=1, padx=10, pady=10, sticky="w")

                def pick_date(var=date_var):
                    CalendarPicker.open(self, lambda date_str: var.set(date_str))

                ttk.Button(self, text="Pick Date", command=pick_date, style="TButton").grid(row=idx, column=2, padx=10, pady=10, sticky="w")
                self.entries[label_text] = date_var

            elif field_schema["type"] == "time":
                time_var = tk.StringVar()
                ttk.Entry(self, textvariable=time_var, state="readonly", style="TEntry").grid(row=idx, column=1, padx=10, pady=10, sticky="w")

                def pick_time(var=time_var):
                    TimePicker.open(self, lambda time_str: var.set(time_str))

                ttk.Button(self, text="Pick Time", command=pick_time, style="TButton").grid(row=idx, column=2, padx=10, pady=10, sticky="w")
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

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Settings", menu=file_menu)

        employee_settings = tk.Menu(menubar, tearoff=0)
        employee_settings.add_command(label="Add Employee")
        employee_settings.add_command(label="View Employees")
        employee_settings.add_command(label="Delete Employee")
        menubar.add_cascade(label="Employee Settings", menu=employee_settings)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def create_nav(self):
        try:
            image = Image.open("mylogo.png")
            image = image.resize((200, 50), Image.LANCZOS)

            background = Image.new("RGB", (200, 50), "white")
            background.paste(image, (0, 0), image)

            photo = ImageTk.PhotoImage(background)

            top_frame = ttk.Frame(self, style="TopFrame.TFrame")
            top_frame.pack(side="top", fill="x")

            style = ttk.Style()
            style.configure("TopFrame.TFrame", background="white")

            logo_label = ttk.Label(top_frame, image=photo, background="white")
            logo_label.image = photo
            logo_label.pack(side="left", anchor="nw")

        except FileNotFoundError:
            print("Logo file not found.")

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
            "Name": {"type": "combobox", "values": load_people},
            "In Time": {"type": "time"},
            "Out Time": {"type": "time"},
            "Date": {"type": "calendar"},
            "Term": {"type": "entry"},
            "Week": {"type": "entry"},
            "Break": {"type": "entry"}
        }
        self.form = DynamicForm(self.add_record_frame, form_items)
        self.form.pack(pady=20, padx=20)

        button_frame = ttk.Frame(self.add_record_frame)
        button_frame.pack(pady=10)

        save_button = ttk.Button(button_frame, text="Save", command=self.save_record)
        save_button.grid(row=0, column=0, padx=10)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_form)
        clear_button.grid(row=0, column=1, padx=10)

    def create_view_records_table(self):
        for widget in self.view_records_frame.winfo_children():
            widget.destroy()

        # Create a frame to hold the title and dropdown
        header_frame = ttk.Frame(self.view_records_frame)
        header_frame.pack(fill="x", pady=10, padx=10)

        # Title label on the left
        title_label = ttk.Label(header_frame, text="Timesheet Records", font=("Arial", 16))
        title_label.pack(side="left", anchor="w")

        try:
            with open("timesheet_records.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            if rows:
                columns = list(rows[0].keys())
            else:
                columns = []

            if not columns:
                ttk.Label(self.view_records_frame, text="No records found in the file.").pack(pady=20)
                return
        except FileNotFoundError:
            ttk.Label(self.view_records_frame, text="No records file found.").pack(pady=20)
            return
        except csv.Error:
            ttk.Label(self.view_records_frame, text="An error occurred while reading the records file.").pack(pady=20)
            return
        except Exception as e:
            ttk.Label(self.view_records_frame, text=f"An error occurred: {e}").pack(pady=20)
            return

        employee_list = ["All"]  # Default option
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                employee_list.extend(data.get("people", []))
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass

        employee_var = tk.StringVar(value="All")
        employee_dropdown = ttk.Combobox(header_frame, textvariable=employee_var, values=employee_list, state="readonly")
        employee_dropdown.pack(side="right", anchor="e")

        try:
            table_frame = ttk.Frame(self.view_records_frame)
            table_frame.pack(fill="both", expand=True)

            table = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
            table.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
            table.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            for col in columns:
                table.heading(col, text=col, anchor="center")
                table.column(col, anchor="center", width=100)

            for row in rows:
                table.insert("", "end", values=[row[col] for col in columns])

        except FileNotFoundError:
            ttk.Label(self.view_records_frame, text="No records file found.").pack(pady=20)

    def save_record(self):
        values = self.form.get_values()

        for key, value in values.items():
            if not value.strip():
                messagebox.showerror("Incomplete Form", f"Please fill in the '{key}' field.")
                return

        term = values.get("Term")
        week = values.get("Week")
        date = values.get("Date")
        name = values.get("Name")
        in_time = values.get("In Time")
        out_time = values.get("Out Time")
        break_time = values.get("Break")

        try:
            in_time_obj = datetime.datetime.strptime(in_time, "%I:%M %p").time()
            out_time_obj = datetime.datetime.strptime(out_time, "%I:%M %p").time()
        except ValueError:
            messagebox.showerror("Invalid Time", "Please ensure both times are correctly selected.")
            return

        if in_time_obj >= out_time_obj:
            messagebox.showerror("Invalid Time Range", "In Time must be earlier than Out Time.")
            return

        try:
            with open("timesheet_records.csv", "a", newline="") as file:
                writer = csv.writer(file)

                if file.tell() == 0:
                    writer.writerow(["Term", "Week", "Date", "Name", "In Time", "Out Time", "Break"])

                writer.writerow([term, week, date, name, in_time, out_time, break_time])

            messagebox.showinfo("Success", "Data recorded successfully!")
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the record: {e}")

    def clear_form(self):
        for entry in self.form.entries.values():
            if isinstance(entry, tk.StringVar):
                entry.set("")
            elif isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()