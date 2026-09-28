import tkinter as tk
from tkinter import messagebox
import json
import os

# This automatically finds the exact folder where your script is saved
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================================================
# FILE NAMES
# =========================================================

PROFILE_FILE = "student_profile.json"
ATTENDANCE_FILE = "attendance.json"
ASSIGNMENT_FILE = "assignments.json"
STUDY_FILE = "study_planner.json"
CGPA_FILE = "cgpa.json"
NOTICE_FILE = "notices.json"


# =========================================================
# GENERAL JSON FUNCTIONS
# =========================================================

def load_json(filename, default):
    filepath = os.path.join(SCRIPT_DIR, filename)

    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return default

    return default


def save_json(filename, data):
    filepath = os.path.join(SCRIPT_DIR, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except PermissionError:
        messagebox.showerror(
            "Permission Denied",
            "Python does not have permission to save files in:\n\n"
            + SCRIPT_DIR
            + "\n\n"
            "Please move the program to a folder where you have write permission."
        )

    except OSError as e:
        messagebox.showerror(
            "File Error",
            "Could not save the file.\n\n"
            + str(e)
        )



# =========================================================
# 1. STUDENT PROFILE
# =========================================================

def open_profile():

    window = tk.Toplevel(root)
    window.title("Student Profile")
    window.geometry("500x500")
    window.resizable(False, False)

    tk.Label(
        window,
        text="STUDENT PROFILE",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    form = tk.Frame(window)
    form.pack()

    labels = [
        "Student Name:",
        "Roll Number:",
        "Branch:",
        "Semester:",
        "College:"
    ]

    entries = []

    for i, label in enumerate(labels):

        tk.Label(
            form,
            text=label,
            font=("Arial", 11)
        ).grid(row=i, column=0, padx=10, pady=10, sticky="w")

        entry = tk.Entry(form, width=30)
        entry.grid(row=i, column=1, padx=10, pady=10)

        entries.append(entry)

    name_entry = entries[0]
    roll_entry = entries[1]
    branch_entry = entries[2]
    semester_entry = entries[3]
    college_entry = entries[4]

    # Load previous profile
    profile = load_json(PROFILE_FILE, {})

    name_entry.insert(0, profile.get("name", ""))
    roll_entry.insert(0, profile.get("roll", ""))
    branch_entry.insert(0, profile.get("branch", ""))
    semester_entry.insert(0, profile.get("semester", ""))
    college_entry.insert(0, profile.get("college", ""))

    def save_profile():

        name = name_entry.get().strip()
        roll = roll_entry.get().strip()
        branch = branch_entry.get().strip()
        semester = semester_entry.get().strip()
        college = college_entry.get().strip()

        if not name or not roll or not branch or not semester or not college:
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        data = {
            "name": name,
            "roll": roll,
            "branch": branch,
            "semester": semester,
            "college": college
        }

        save_json(PROFILE_FILE, data)

        messagebox.showinfo(
            "Success",
            "Student profile saved successfully!"
        )

    tk.Button(
        window,
        text="Save Profile",
        width=20,
        height=2,
        command=save_profile
    ).pack(pady=20)


# =========================================================
# 2. ATTENDANCE
# =========================================================

def open_attendance():

    window = tk.Toplevel(root)
    window.title("Attendance Manager")
    window.geometry("750x600")
    window.resizable(False, False)

    tk.Label(
        window,
        text="ATTENDANCE MANAGER",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    form = tk.Frame(window)
    form.pack()

    # Subject
    tk.Label(form, text="Subject:").grid(
        row=0, column=0, padx=10, pady=8
    )

    subject_entry = tk.Entry(form, width=30)
    subject_entry.grid(row=0, column=1, padx=10, pady=8)

    # Classes held
    tk.Label(form, text="Classes Held:").grid(
        row=1, column=0, padx=10, pady=8
    )

    held_entry = tk.Entry(form, width=30)
    held_entry.grid(row=1, column=1, padx=10, pady=8)

    # Classes attended
    tk.Label(form, text="Classes Attended:").grid(
        row=2, column=0, padx=10, pady=8
    )

    attended_entry = tk.Entry(form, width=30)
    attended_entry.grid(row=2, column=1, padx=10, pady=8)

    attendance_list = tk.Listbox(
        window,
        width=90,
        height=12
    )
    attendance_list.pack(pady=20)

    def display():

        attendance_list.delete(0, tk.END)

        data = load_json(ATTENDANCE_FILE, [])

        for i, item in enumerate(data):

            text = (
                str(i + 1)
                + ". "
                + item["subject"]
                + " | Held: "
                + str(item["held"])
                + " | Attended: "
                + str(item["attended"])
                + " | "
                + str(item["percentage"])
                + "%"
            )

            attendance_list.insert(tk.END, text)

    def add():

        subject = subject_entry.get().strip()
        held = held_entry.get().strip()
        attended = attended_entry.get().strip()

        if not subject or not held or not attended:
            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )
            return

        try:
            held = int(held)
            attended = int(attended)
        except ValueError:
            messagebox.showwarning(
                "Invalid Data",
                "Please enter numbers."
            )
            return

        if held <= 0 or attended < 0 or attended > held:
            messagebox.showwarning(
                "Invalid Data",
                "Please enter valid attendance numbers."
            )
            return

        percentage = round((attended / held) * 100, 2)

        data = load_json(ATTENDANCE_FILE, [])

        data.append({
            "subject": subject,
            "held": held,
            "attended": attended,
            "percentage": percentage
        })

        save_json(ATTENDANCE_FILE, data)

        subject_entry.delete(0, tk.END)
        held_entry.delete(0, tk.END)
        attended_entry.delete(0, tk.END)

        display()

    def delete():

        selected = attendance_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a subject first."
            )
            return

        index = selected[0]

        data = load_json(ATTENDANCE_FILE, [])

        data.pop(index)

        save_json(ATTENDANCE_FILE, data)

        display()

    buttons = tk.Frame(window)
    buttons.pack()

    tk.Button(
        buttons,
        text="Add Attendance",
        width=18,
        command=add
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        buttons,
        text="Delete",
        width=18,
        command=delete
    ).grid(row=0, column=1, padx=5)

    display()


# =========================================================
# 3. ASSIGNMENTS
# =========================================================

def open_assignments():

    window = tk.Toplevel(root)
    window.title("Assignment Manager")
    window.geometry("800x600")
    window.resizable(False, False)

    tk.Label(
        window,
        text="ASSIGNMENT MANAGER",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    form = tk.Frame(window)
    form.pack()

    # Subject
    tk.Label(form, text="Subject:").grid(
        row=0, column=0, padx=10, pady=8
    )

    subject_entry = tk.Entry(form, width=35)
    subject_entry.grid(row=0, column=1, padx=10, pady=8)

    # Assignment
    tk.Label(form, text="Assignment Name:").grid(
        row=1, column=0, padx=10, pady=8
    )

    title_entry = tk.Entry(form, width=35)
    title_entry.grid(row=1, column=1, padx=10, pady=8)

    # Due date
    tk.Label(form, text="Due Date:").grid(
        row=2, column=0, padx=10, pady=8
    )

    date_entry = tk.Entry(form, width=35)
    date_entry.grid(row=2, column=1, padx=10, pady=8)

    assignment_list = tk.Listbox(
        window,
        width=95,
        height=12
    )
    assignment_list.pack(pady=20)

    def display():

        assignment_list.delete(0, tk.END)

        data = load_json(ASSIGNMENT_FILE, [])

        for i, item in enumerate(data):

            text = (
                str(i + 1)
                + ". "
                + item["subject"]
                + " | "
                + item["title"]
                + " | Due: "
                + item["due_date"]
                + " | "
                + item["status"]
            )

            assignment_list.insert(tk.END, text)

    def add():

        subject = subject_entry.get().strip()
        title = title_entry.get().strip()
        due_date = date_entry.get().strip()

        if not subject or not title or not due_date:
            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )
            return

        data = load_json(ASSIGNMENT_FILE, [])

        data.append({
            "subject": subject,
            "title": title,
            "due_date": due_date,
            "status": "Pending"
        })

        save_json(ASSIGNMENT_FILE, data)

        subject_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)

        display()

    def complete():

        selected = assignment_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select an assignment first."
            )
            return

        index = selected[0]

        data = load_json(ASSIGNMENT_FILE, [])

        data[index]["status"] = "Completed"

        save_json(ASSIGNMENT_FILE, data)

        display()

    def delete():

        selected = assignment_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select an assignment first."
            )
            return

        index = selected[0]

        data = load_json(ASSIGNMENT_FILE, [])

        data.pop(index)

        save_json(ASSIGNMENT_FILE, data)

        display()

    buttons = tk.Frame(window)
    buttons.pack()

    tk.Button(
        buttons,
        text="Add Assignment",
        width=18,
        command=add
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        buttons,
        text="Mark Completed",
        width=18,
        command=complete
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        buttons,
        text="Delete",
        width=18,
        command=delete
    ).grid(row=0, column=2, padx=5)

    display()


# =========================================================
# 4. STUDY PLANNER
# =========================================================

def open_study_planner():

    window = tk.Toplevel(root)
    window.title("Study Planner")
    window.geometry("800x600")
    window.resizable(False, False)

    tk.Label(
        window,
        text="STUDY PLANNER",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    form = tk.Frame(window)
    form.pack()

    # Subject
    tk.Label(form, text="Subject:").grid(
        row=0, column=0, padx=10, pady=8
    )

    subject_entry = tk.Entry(form, width=35)
    subject_entry.grid(row=0, column=1, padx=10, pady=8)

    # Task
    tk.Label(form, text="Study Task:").grid(
        row=1, column=0, padx=10, pady=8
    )

    task_entry = tk.Entry(form, width=35)
    task_entry.grid(row=1, column=1, padx=10, pady=8)

    # Date
    tk.Label(form, text="Study Date:").grid(
        row=2, column=0, padx=10, pady=8
    )

    date_entry = tk.Entry(form, width=35)
    date_entry.grid(row=2, column=1, padx=10, pady=8)

    # Priority
    tk.Label(form, text="Priority:").grid(
        row=3, column=0, padx=10, pady=8
    )

    priority_var = tk.StringVar()
    priority_var.set("Medium")

    priority_menu = tk.OptionMenu(
        form,
        priority_var,
        "High",
        "Medium",
        "Low"
    )

    priority_menu.grid(
        row=3,
        column=1,
        padx=10,
        pady=8
    )

    study_list = tk.Listbox(
        window,
        width=95,
        height=12
    )
    study_list.pack(pady=20)

    def display():

        study_list.delete(0, tk.END)

        data = load_json(STUDY_FILE, [])

        for i, item in enumerate(data):

            text = (
                str(i + 1)
                + ". "
                + item["subject"]
                + " | "
                + item["task"]
                + " | Date: "
                + item["date"]
                + " | Priority: "
                + item["priority"]
                + " | "
                + item["status"]
            )

            study_list.insert(tk.END, text)

    def add():

        subject = subject_entry.get().strip()
        task = task_entry.get().strip()
        date = date_entry.get().strip()
        priority = priority_var.get()

        if not subject or not task or not date:
            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )
            return

        data = load_json(STUDY_FILE, [])

        data.append({
            "subject": subject,
            "task": task,
            "date": date,
            "priority": priority,
            "status": "Pending"
        })

        save_json(STUDY_FILE, data)

        subject_entry.delete(0, tk.END)
        task_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)

        display()

    def complete():

        selected = study_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a task first."
            )
            return

        index = selected[0]

        data = load_json(STUDY_FILE, [])

        data[index]["status"] = "Completed"

        save_json(STUDY_FILE, data)

        display()

    def delete():

        selected = study_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a task first."
            )
            return

        index = selected[0]

        data = load_json(STUDY_FILE, [])

        data.pop(index)

        save_json(STUDY_FILE, data)

        display()

    buttons = tk.Frame(window)
    buttons.pack()

    tk.Button(
        buttons,
        text="Add Study Task",
        width=18,
        command=add
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        buttons,
        text="Mark Completed",
        width=18,
        command=complete
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        buttons,
        text="Delete",
        width=18,
        command=delete
    ).grid(row=0, column=2, padx=5)

    display()


# =========================================================
# 5. CGPA CALCULATOR
# =========================================================

def open_cgpa():

    window = tk.Toplevel(root)
    window.title("CGPA Calculator")
    window.geometry("750x600")
    window.resizable(False, False)

    tk.Label(
        window,
        text="CGPA CALCULATOR",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    tk.Label(
        window,
        text="Enter grade point between 0 and 10",
        font=("Arial", 11)
    ).pack()

    form = tk.Frame(window)
    form.pack(pady=10)

    # Subject
    tk.Label(form, text="Subject:").grid(
        row=0, column=0, padx=10, pady=8
    )

    subject_entry = tk.Entry(form, width=25)
    subject_entry.grid(row=0, column=1, padx=10, pady=8)

    # Credits
    tk.Label(form, text="Credits:").grid(
        row=1, column=0, padx=10, pady=8
    )

    credit_entry = tk.Entry(form, width=25)
    credit_entry.grid(row=1, column=1, padx=10, pady=8)

    # Grade point
    tk.Label(form, text="Grade Point:").grid(
        row=2, column=0, padx=10, pady=8
    )

    grade_entry = tk.Entry(form, width=25)
    grade_entry.grid(row=2, column=1, padx=10, pady=8)

    cgpa_list = tk.Listbox(
        window,
        width=80,
        height=10
    )
    cgpa_list.pack(pady=15)

    result_label = tk.Label(
        window,
        text="CGPA: 0.00",
        font=("Arial", 16, "bold")
    )
    result_label.pack(pady=10)

    def display():

        cgpa_list.delete(0, tk.END)

        data = load_json(CGPA_FILE, [])

        for i, item in enumerate(data):

            text = (
                str(i + 1)
                + ". "
                + item["subject"]
                + " | Credits: "
                + str(item["credits"])
                + " | Grade Point: "
                + str(item["grade_point"])
            )

            cgpa_list.insert(tk.END, text)

    def add_subject():

        subject = subject_entry.get().strip()
        credits = credit_entry.get().strip()
        grade = grade_entry.get().strip()

        if not subject or not credits or not grade:
            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )
            return

        try:
            credits = float(credits)
            grade = float(grade)
        except ValueError:
            messagebox.showwarning(
                "Invalid Data",
                "Credits and grade point must be numbers."
            )
            return

        if credits <= 0:
            messagebox.showwarning(
                "Invalid Data",
                "Credits must be greater than 0."
            )
            return

        if grade < 0 or grade > 10:
            messagebox.showwarning(
                "Invalid Data",
                "Grade point must be between 0 and 10."
            )
            return

        data = load_json(CGPA_FILE, [])

        data.append({
            "subject": subject,
            "credits": credits,
            "grade_point": grade
        })

        save_json(CGPA_FILE, data)

        subject_entry.delete(0, tk.END)
        credit_entry.delete(0, tk.END)
        grade_entry.delete(0, tk.END)

        display()

    def calculate_cgpa():

        data = load_json(CGPA_FILE, [])

        if not data:
            messagebox.showwarning(
                "No Data",
                "Add subjects first."
            )
            return

        total_credits = 0
        total_points = 0

        for item in data:

            credits = item["credits"]
            grade = item["grade_point"]

            total_credits += credits
            total_points += credits * grade

        cgpa = total_points / total_credits

        result_label.config(
            text="CGPA: " + str(round(cgpa, 2))
        )

    def delete_subject():

        selected = cgpa_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a subject first."
            )
            return

        index = selected[0]

        data = load_json(CGPA_FILE, [])

        data.pop(index)

        save_json(CGPA_FILE, data)

        display()

        result_label.config(
            text="CGPA: 0.00"
        )

    buttons = tk.Frame(window)
    buttons.pack(pady=5)

    tk.Button(
        buttons,
        text="Add Subject",
        width=16,
        command=add_subject
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        buttons,
        text="Calculate CGPA",
        width=16,
        command=calculate_cgpa
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        buttons,
        text="Delete",
        width=16,
        command=delete_subject
    ).grid(row=0, column=2, padx=5)

    display()


# =========================================================
# 6. COLLEGE NOTICE BOARD
# =========================================================

def open_notices():

    window = tk.Toplevel(root)
    window.title("College Notice Board")
    window.geometry("800x650")
    window.resizable(False, False)

    tk.Label(
        window,
        text="COLLEGE NOTICE BOARD",
        font=("Arial", 22, "bold")
    ).pack(pady=20)

    form = tk.Frame(window)
    form.pack()

    # Notice title
    tk.Label(form, text="Notice Title:").grid(
        row=0, column=0, padx=10, pady=8
    )

    title_entry = tk.Entry(form, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=8)

    # Date
    tk.Label(form, text="Date:").grid(
        row=1, column=0, padx=10, pady=8
    )

    date_entry = tk.Entry(form, width=40)
    date_entry.grid(row=1, column=1, padx=10, pady=8)

    # Notice
    tk.Label(form, text="Notice:").grid(
        row=2, column=0, padx=10, pady=8
    )

    notice_entry = tk.Entry(form, width=40)
    notice_entry.grid(row=2, column=1, padx=10, pady=8)

    notice_list = tk.Listbox(
        window,
        width=95,
        height=15
    )
    notice_list.pack(pady=20)

    def display():

        notice_list.delete(0, tk.END)

        data = load_json(NOTICE_FILE, [])

        for i, item in enumerate(data):

            text = (
                str(i + 1)
                + ". "
                + item["title"]
                + " | "
                + item["date"]
                + " | "
                + item["notice"]
            )

            notice_list.insert(tk.END, text)

    def add_notice():

        title = title_entry.get().strip()
        date = date_entry.get().strip()
        notice = notice_entry.get().strip()

        if not title or not date or not notice:
            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )
            return

        data = load_json(NOTICE_FILE, [])

        data.append({
            "title": title,
            "date": date,
            "notice": notice
        })

        save_json(NOTICE_FILE, data)

        title_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        notice_entry.delete(0, tk.END)

        display()

    def delete_notice():

        selected = notice_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a notice first."
            )
            return

        index = selected[0]

        data = load_json(NOTICE_FILE, [])

        data.pop(index)

        save_json(NOTICE_FILE, data)

        display()

    buttons = tk.Frame(window)
    buttons.pack()

    tk.Button(
        buttons,
        text="Add Notice",
        width=18,
        command=add_notice
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        buttons,
        text="Delete Notice",
        width=18,
        command=delete_notice
    ).grid(row=0, column=1, padx=5)

    display()


# =========================================================
# MAIN DASHBOARD
# =========================================================

root = tk.Tk()

root.title("Smart Student Manager")

root.geometry("700x750")

root.resizable(False, False)


# Heading

tk.Label(
    root,
    text="SMART STUDENT MANAGER",
    font=("Arial", 26, "bold")
).pack(pady=25)


tk.Label(
    root,
    text="College Student Management System",
    font=("Arial", 12)
).pack()


# Buttons

button_frame = tk.Frame(root)
button_frame.pack(pady=25)


tk.Button(
    button_frame,
    text="Student Profile",
    width=30,
    height=2,
    font=("Arial", 12),
    command=open_profile
).pack(pady=7)


tk.Button(
    button_frame,
    text="Attendance",
    width=30,
    height=2,
    font=("Arial", 12),
    command=open_attendance
).pack(pady=7)


tk.Button(
    button_frame,
    text="Assignments",
    width=30,
    height=2,
    font=("Arial", 12),
    command=open_assignments
).pack(pady=7)


tk.Button(
    button_frame,
    text="Study Planner",
    width=30,
    height=2,
    font=("Arial", 12),
    command=open_study_planner
).pack(pady=7)


tk.Button(
    button_frame,
    text="CGPA Calculator",
    width=30,
    height=2,
    font=("Arial", 12),
    command=open_cgpa
).pack(pady=7)


tk.Button(
    button_frame,
    text="College Notice Board",
    width=30,
    height=2,
    font=("Arial", 12),
    command=open_notices
).pack(pady=7)


tk.Button(
    button_frame,
    text="Exit",
    width=30,
    height=2,
    font=("Arial", 12),
    command=root.destroy
).pack(pady=15)


# Start application

root.mainloop()
