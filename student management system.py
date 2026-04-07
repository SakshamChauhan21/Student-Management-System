import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "students.json"
students = {}

# ---------------- File Handling ----------------
def load_data():
    global students
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                students = json.load(file)
        except:
            students = {}
    else:
        students = {}

def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)

# ---------------- Functions ----------------
def add_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()

    if not roll or not name or not age or not course:
        messagebox.showwarning("Warning", "All fields are required!")
        return

    if roll in students:
        messagebox.showerror("Error", "Student already exists!")
        return

    students[roll] = {"Name": name, "Age": age, "Course": course}
    save_data()
    show_students()
    clear_fields()
    messagebox.showinfo("Success", "Student added successfully!")

def update_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    course = course_entry.get().strip()

    if not roll or not name or not age or not course:
        messagebox.showwarning("Warning", "All fields are required!")
        return

    if roll not in students:
        messagebox.showerror("Error", "Student not found!")
        return

    students[roll] = {"Name": name, "Age": age, "Course": course}
    save_data()
    show_students()
    clear_fields()
    messagebox.showinfo("Success", "Student updated successfully!")

def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student!")
        return

    values = tree.item(selected, "values")
    roll = values[0]

    confirm = messagebox.askyesno("Confirm Delete", f"Delete student {roll}?")
    if confirm:
        if roll in students:
            del students[roll]
            save_data()
            show_students()
            clear_fields()
            messagebox.showinfo("Deleted", "Student deleted successfully!")

def search_student():
    keyword = search_entry.get().strip().lower()
    tree.delete(*tree.get_children())

    for roll, details in students.items():
        if (keyword in roll.lower() or
            keyword in details["Name"].lower() or
            keyword in details["Age"].lower() or
            keyword in details["Course"].lower()):
            tree.insert("", tk.END, values=(roll, details["Name"], details["Age"], details["Course"]))

def show_students():
    tree.delete(*tree.get_children())
    for roll, details in students.items():
        tree.insert("", tk.END, values=(roll, details["Name"], details["Age"], details["Course"]))

def clear_fields():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

def fill_form(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")
    clear_fields()
    roll_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    course_entry.insert(0, values[3])

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Student Management System")
root.geometry("950x620")
root.configure(bg="#0f172a")
root.resizable(False, False)

# Style
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#1e293b",
                foreground="white",
                rowheight=28,
                fieldbackground="#1e293b",
                bordercolor="#1e293b",
                borderwidth=0,
                font=("Segoe UI", 10))

style.configure("Treeview.Heading",
                background="#334155",
                foreground="white",
                font=("Segoe UI", 11, "bold"),
                relief="flat")

style.map("Treeview",
          background=[("selected", "#3b82f6")])

# Title
title = tk.Label(root,
                 text="Student Management System",
                 font=("Segoe UI", 24, "bold"),
                 bg="#0f172a",
                 fg="white")
title.pack(pady=15)

# Top Frame
top_frame = tk.Frame(root, bg="#0f172a")
top_frame.pack(fill="x", padx=20)

# Form Frame
form_frame = tk.Frame(top_frame, bg="#111827", bd=0, relief="flat")
form_frame.pack(side="left", padx=10, pady=10)

def make_label(text, row, col=0):
    tk.Label(form_frame, text=text,
             bg="#111827", fg="#e5e7eb",
             font=("Segoe UI", 11, "bold")).grid(row=row, column=col, padx=12, pady=10, sticky="w")

def make_entry(row, col=1):
    entry = tk.Entry(form_frame,
                     font=("Segoe UI", 11),
                     bg="#1f2937", fg="white",
                     insertbackground="white",
                     relief="flat", width=28)
    entry.grid(row=row, column=col, padx=12, pady=10, ipady=6)
    return entry

make_label("Roll No", 0)
roll_entry = make_entry(0)

make_label("Name", 1)
name_entry = make_entry(1)

make_label("Age", 2)
age_entry = make_entry(2)

make_label("Course", 3)
course_entry = make_entry(3)

# Search Frame
search_frame = tk.Frame(top_frame, bg="#111827")
search_frame.pack(side="right", padx=10, pady=10, fill="y")

tk.Label(search_frame, text="Search Student",
         bg="#111827", fg="white",
         font=("Segoe UI", 14, "bold")).pack(pady=(15, 10))

search_entry = tk.Entry(search_frame,
                        font=("Segoe UI", 11),
                        bg="#1f2937", fg="white",
                        insertbackground="white",
                        relief="flat", width=28)
search_entry.pack(padx=20, pady=8, ipady=6)

# Button function
def make_button(parent, text, command, color, width=15):
    return tk.Button(parent,
                     text=text,
                     command=command,
                     bg=color,
                     fg="white",
                     activebackground=color,
                     activeforeground="white",
                     relief="flat",
                     bd=0,
                     font=("Segoe UI", 10, "bold"),
                     width=width,
                     pady=8,
                     cursor="hand2")

make_button(search_frame, "Search", search_student, "#2563eb").pack(pady=8)
make_button(search_frame, "Show All", show_students, "#475569").pack(pady=8)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#0f172a")
btn_frame.pack(pady=10)

make_button(btn_frame, "Add", add_student, "#16a34a").grid(row=0, column=0, padx=8)
make_button(btn_frame, "Update", update_student, "#d97706").grid(row=0, column=1, padx=8)
make_button(btn_frame, "Delete", delete_student, "#dc2626").grid(row=0, column=2, padx=8)
make_button(btn_frame, "Clear", clear_fields, "#6b7280").grid(row=0, column=3, padx=8)

# Table Frame
table_frame = tk.Frame(root, bg="#0f172a")
table_frame.pack(padx=20, pady=15, fill="both", expand=True)

tree_scroll = tk.Scrollbar(table_frame)
tree_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(table_frame,
                    yscrollcommand=tree_scroll.set,
                    columns=("Roll", "Name", "Age", "Course"),
                    show="headings",
                    height=14)

tree_scroll.config(command=tree.yview)

tree.heading("Roll", text="Roll No")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Course", text="Course")

tree.column("Roll", width=120, anchor="center")
tree.column("Name", width=250, anchor="center")
tree.column("Age", width=100, anchor="center")
tree.column("Course", width=200, anchor="center")

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", fill_form)

# Load existing data
load_data()
show_students()

root.mainloop()