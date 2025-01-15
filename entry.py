import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
import csv
import os
import datetime

# File to store data
FILE_NAME = "data_entry.csv"

# Create the CSV file if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Term", "Week", "Date", "Day", "Name", "In Time", "Out Time", "Break"])  # Headers

# Function to add data
def add_data():
    term = term_var.get()
    week = week_var.get()
    selected_date = date_var.get()
    day = day_var.get()
    name = name_var.get()
    in_time = in_time_var.get()
    out_time = out_time_var.get()
    break_time = break_var.get()

    if not (term and week and selected_date and day and name and in_time and out_time and break_time):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([term, week, selected_date, day, name, in_time, out_time, break_time])

    messagebox.showinfo("Success", "Data recorded successfully!")
    # Clear all input fields
    term_var.set("")
    week_var.set("")
    date_var.set("")
    day_var.set("")
    name_var.set("")
    in_time_var.set("")
    out_time_var.set("")
    break_var.set("")

# Function to view records
def view_records():
    try:
        with open(FILE_NAME, "r") as file:
            records = file.readlines()

        if len(records) <= 1:
            messagebox.showinfo("No Records", "No data records found!")
            return

        # Display records in a new window
        view_window = tk.Toplevel(root)
        view_window.title("Data Records")
        view_window.geometry("800x400")

        # Configure the text area to display records
        text_area = tk.Text(view_window, wrap="none", bg="#333", fg="#fff", font=("Arial", 12))
        text_area.insert("1.0", "".join(records))  # Insert records into the text area
        text_area.pack(expand=True, fill="both")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to read records: {e}")

# Function to open a calendar and update the date and day
def open_calendar():
    def select_date():
        selected_date = cal.get_date()
        date_var.set(selected_date)

        # Get the day from the selected date
        selected_date_obj = datetime.datetime.strptime(selected_date, "%m/%d/%y")
        day_name = selected_date_obj.strftime("%A")
        day_var.set(day_name)

        calendar_window.destroy()

    calendar_window = tk.Toplevel(root)
    calendar_window.title("Select Date")
    cal = Calendar(calendar_window, selectmode="day", date_pattern="mm/dd/yy")
    cal.pack(pady=20)

    ttk.Button(calendar_window, text="Select", command=select_date).pack(pady=10)

# Function to show the entry form
def show_entry_form():
    entry_frame.pack_forget()  # Hide the current frame
    view_frame.pack_forget()  # Hide the current frame

    entry_frame.pack(expand=True)  # Show the entry form

# Function to show the view records
def show_view_records():
    entry_frame.pack_forget()  # Hide the current frame
    view_frame.pack_forget()  # Hide the current frame

    view_frame.pack(expand=True)  # Show the view records frame

# Main application window
root = tk.Tk()
root.title("Data Entry System")
root.geometry("800x600+300+150")  # Centered on the screen
root.configure(bg="#222")

# Load image
img = Image.open("mylogo.png")  # Replace with your image file
img = img.resize((img.width, img.height))  # Maintain original size
img_tk = ImageTk.PhotoImage(img)

# Display image at the top
img_label = tk.Label(root, image=img_tk, bg="#222")
img_label.pack(pady=20)

# Create buttons to switch between forms
button_frame = tk.Frame(root, bg="#222")
button_frame.pack()

entry_button = tk.Button(button_frame, text="Entry", command=show_entry_form, bg="#4CAF50", fg="#fff", font=("Arial", 14))
entry_button.pack(side="left", padx=10)

view_button = tk.Button(button_frame, text="View Records", command=show_view_records, bg="#4CAF50", fg="#fff", font=("Arial", 14))
view_button.pack(side="left", padx=10)

# Create entry form frame
entry_frame = tk.Frame(root, bg="#222")

# Input Variables
term_var = tk.StringVar()
week_var = tk.StringVar()
date_var = tk.StringVar()
day_var = tk.StringVar()
name_var = tk.StringVar()
in_time_var = tk.StringVar()
out_time_var = tk.StringVar()
break_var = tk.StringVar()

# Dropdown options for names
names_list = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown"]  # Add more names as needed

# Input Fields (Left Column)
left_frame = tk.Frame(entry_frame, bg="#222")
left_frame.grid(row=0, column=0, padx=20, pady=20)

tk.Label(left_frame, text="Term:", bg="#222", fg="#fff", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
tk.Entry(left_frame, textvariable=term_var, font=("Arial", 12), width=30).grid(row=0, column=1, padx=10, pady=10)

tk.Label(left_frame, text="Week:", bg="#222", fg="#fff", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Entry(left_frame, textvariable=week_var, font=("Arial", 12), width=30).grid(row=1, column=1, padx=10, pady=10)

tk.Label(left_frame, text="Date:", bg="#222", fg="#fff", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
tk.Entry(left_frame, textvariable=date_var, font=("Arial", 12), width=30, state="readonly").grid(row=2, column=1, padx=10, pady=10)
tk.Button(left_frame, text="Select Date", command=open_calendar, bg="#4CAF50", fg="#fff", font=("Arial", 10)).grid(row=2, column=2, padx=10)

tk.Label(left_frame, text="Day:", bg="#222", fg="#fff", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
tk.Entry(left_frame, textvariable=day_var, font=("Arial", 12), width=30, state="readonly").grid(row=3, column=1, padx=10, pady=10)

# Input Fields (Right Column)
right_frame = tk.Frame(entry_frame, bg="#222")
right_frame.grid(row=0, column=1, padx=20, pady=20)

tk.Label(right_frame, text="Name:", bg="#222", fg="#fff", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
name_dropdown = ttk.Combobox(right_frame, textvariable=name_var, values=names_list, font=("Arial", 12), width=28)
name_dropdown.grid(row=0, column=1, padx=10, pady=10)

# Time Picker (In Time)
tk.Label(right_frame, text="In Time:", bg="#222", fg="#fff", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")

hours = [str(i).zfill(2) for i in range(1, 13)]
minutes = [str(i).zfill(2) for i in range(0, 60, 5)]
am_pm = ["AM", "PM"]

in_time_hour = ttk.Combobox(right_frame, values=hours, width=5, font=("Arial", 12))
in_time_hour.grid(row=1, column=1, padx=5, pady=10)
in_time_minute = ttk.Combobox(right_frame, values=minutes, width=5, font=("Arial", 12))
in_time_minute.grid(row=1, column=2, padx=5, pady=10)
in_time_am_pm = ttk.Combobox(right_frame, values=am_pm, width=5, font=("Arial", 12))
in_time_am_pm.grid(row=1, column=3, padx=5, pady=10)

# Time Picker (Out Time)
tk.Label(right_frame, text="Out Time:", bg="#222", fg="#fff", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")

out_time_hour = ttk.Combobox(right_frame, values=hours, width=5, font=("Arial", 12))
out_time_hour.grid(row=2, column=1, padx=5, pady=10)
out_time_minute = ttk.Combobox(right_frame, values=minutes, width=5, font=("Arial", 12))
out_time_minute.grid(row=2, column=2, padx=5, pady=10)
out_time_am_pm = ttk.Combobox(right_frame, values=am_pm, width=5, font=("Arial", 12))
out_time_am_pm.grid(row=2, column=3, padx=5, pady=10)

# Break Input (Entry for Break)
tk.Label(right_frame, text="Break:", bg="#222", fg="#fff", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
tk.Entry(right_frame, textvariable=break_var, font=("Arial", 12), width=28).grid(row=3, column=1, padx=10, pady=10)

# Function to update the time variable when the user selects a time
def update_in_time():
    in_time_var.set(f"{in_time_hour.get()}:{in_time_minute.get()} {in_time_am_pm.get()}")

def update_out_time():
    out_time_var.set(f"{out_time_hour.get()}:{out_time_minute.get()} {out_time_am_pm.get()}")

# Bind the comboboxes to update the time variables
in_time_hour.bind("<<ComboboxSelected>>", lambda event: update_in_time())
in_time_minute.bind("<<ComboboxSelected>>", lambda event: update_in_time())
in_time_am_pm.bind("<<ComboboxSelected>>", lambda event: update_in_time())

out_time_hour.bind("<<ComboboxSelected>>", lambda event: update_out_time())
out_time_minute.bind("<<ComboboxSelected>>", lambda event: update_out_time())
out_time_am_pm.bind("<<ComboboxSelected>>", lambda event: update_out_time())

# Submit Button (Centered)
tk.Button(entry_frame, text="Submit", command=add_data, bg="#4CAF50", fg="#fff", font=("Arial", 14)).grid(row=4, column=0, columnspan=2, pady=20)

# Create view records frame
view_frame = tk.Frame(root, bg="#222")

# Button to view records
tk.Button(view_frame, text="View Records", command=view_records, bg="#4CAF50", fg="#fff", font=("Arial", 14)).pack(pady=50)

# Show the entry form by default
show_entry_form()

root.mainloop()
