import tkinter as tk
from tkinter import messagebox
import json
import os


# ============================================================
# COLORS
# ============================================================

BG = "#F6F7FB"
CARD = "#FFFFFF"
PURPLE = "#7357D9"
LIGHT_PURPLE = "#EEEAFE"
BLUE = "#3182CE"
GREEN = "#27AE60"
ORANGE = "#F39C12"
RED = "#E74C3C"
TEXT = "#172B4D"
GRAY = "#64748B"
BORDER = "#D8DDEA"


# ============================================================
# FILES
# ============================================================

STUDENT_FILE = "student_data.json"
ATTENDANCE_FILE = "attendance_data.json"
ASSIGNMENT_FILE = "assignments.json"
PLANNER_FILE = "study_planner.json"
NOTICE_FILE = "notices.json"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Student Management System")
root.geometry("1250x750")
root.minsize(1050, 650)
root.configure(bg=BG)


# ============================================================
# DATA
# ============================================================

attendance_data = {
    "Mathematics": {"attended": 0, "total": 0},
    "Physics": {"attended": 0, "total": 0},
    "Computer Science": {"attended": 0, "total": 0}
}

assignments = []

study_plan = []

notices = []


# ============================================================
# GENERAL FUNCTIONS
# ============================================================

def save_json(filename, data):

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_json(filename, default):

    if os.path.exists(filename):

        try:
            with open(filename, "r") as file:
                return json.load(file)

        except:
            return default

    return default


# ============================================================
# STUDENT PROFILE
# ============================================================

def open_profile():

    window = tk.Toplevel(root)
    window.title("Student Profile")
    window.geometry("550x550")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="STUDENT PROFILE",
        bg=LIGHT_PURPLE,
        fg=TEXT,
        font=("Arial", 20, "bold")
    ).pack(fill="x", pady=20, ipady=10)

    form = tk.Frame(window, bg=CARD)
    form.pack(fill="both", expand=True, padx=30, pady=20)

    labels = [
        "Student Name",
        "Roll Number",
        "Branch",
        "Semester",
        "College"
    ]

    entries = []

    for i, text in enumerate(labels):

        tk.Label(
            form,
            text=text + ":",
            bg=CARD,
            fg=TEXT,
            font=("Arial", 11, "bold")
        ).grid(
            row=i,
            column=0,
            padx=10,
            pady=12,
            sticky="w"
        )

        entry = tk.Entry(
            form,
            font=("Arial", 11),
            width=30
        )

        entry.grid(
            row=i,
            column=1,
            padx=10,
            pady=12,
            ipady=6
        )

        entries.append(entry)

    def save():

        data = {
            "name": entries[0].get(),
            "roll": entries[1].get(),
            "branch": entries[2].get(),
            "semester": entries[3].get(),
            "college": entries[4].get()
        }

        if any(value.strip() == "" for value in data.values()):

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return

        save_json(STUDENT_FILE, data)

        messagebox.showinfo(
            "Saved",
            "Student information saved successfully."
        )

    def load():

        data = load_json(STUDENT_FILE, {})

        if not data:
            return

        for entry in entries:
            entry.delete(0, tk.END)

        entries[0].insert(0, data.get("name", ""))
        entries[1].insert(0, data.get("roll", ""))
        entries[2].insert(0, data.get("branch", ""))
        entries[3].insert(0, data.get("semester", ""))
        entries[4].insert(0, data.get("college", ""))

    def clear():

        for entry in entries:
            entry.delete(0, tk.END)

    buttons = tk.Frame(form, bg=CARD)
    buttons.grid(row=6, column=0, columnspan=2, pady=25)

    tk.Button(
        buttons,
        text="Save Student",
        command=save,
        bg=BLUE,
        fg="white",
        font=("Arial", 10, "bold"),
        width=15,
        relief="flat"
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        buttons,
        text="Load Student",
        command=load,
        bg=GREEN,
        fg="white",
        font=("Arial", 10, "bold"),
        width=15,
        relief="flat"
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        buttons,
        text="Clear",
        command=clear,
        bg=ORANGE,
        fg="white",
        font=("Arial", 10, "bold"),
        width=15,
        relief="flat"
    ).grid(row=0, column=2, padx=5)

    load()


# ============================================================
# ATTENDANCE
# ============================================================

def open_attendance():

    global attendance_data

    attendance_data = load_json(
        ATTENDANCE_FILE,
        attendance_data
    )

    window = tk.Toplevel(root)

    window.title("Attendance Tracker")
    window.geometry("750x600")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="ATTENDANCE TRACKER",
        bg=LIGHT_PURPLE,
        fg=TEXT,
        font=("Arial", 20, "bold")
    ).pack(fill="x", pady=15, ipady=10)

    main = tk.Frame(window, bg=CARD)
    main.pack(fill="both", expand=True, padx=25, pady=20)

    # SUBJECT LIST

    left = tk.Frame(main, bg=CARD)
    left.pack(side="left", fill="both", expand=True, padx=15)

    tk.Label(
        left,
        text="Subjects",
        bg=CARD,
        fg=TEXT,
        font=("Arial", 12, "bold")
    ).pack(anchor="w")

    subject_list = tk.Listbox(
        left,
        font=("Arial", 11),
        height=15
    )

    subject_list.pack(fill="both", expand=True, pady=10)

    for subject in attendance_data:
        subject_list.insert(tk.END, subject)

    # RIGHT SIDE

    right = tk.Frame(main, bg=CARD)
    right.pack(side="right", fill="both", expand=True, padx=15)

    tk.Label(
        right,
        text="Classes Attended",
        bg=CARD,
        fg=TEXT
    ).pack(anchor="w")

    attended = tk.Entry(right)
    attended.pack(fill="x", pady=5)

    tk.Label(
        right,
        text="Total Classes",
        bg=CARD,
        fg=TEXT
    ).pack(anchor="w")

    total = tk.Entry(right)
    total.pack(fill="x", pady=5)

    percentage = tk.Label(
        right,
        text="Attendance: --%",
        bg="#EEF5FF",
        fg=TEXT,
        font=("Arial", 16, "bold"),
        pady=15
    )

    percentage.pack(fill="x", pady=20)

    def select_subject(event=None):

        selected = subject_list.curselection()

        if not selected:
            return

        subject = subject_list.get(selected[0])

        data = attendance_data[subject]

        attended.delete(0, tk.END)
        total.delete(0, tk.END)

        attended.insert(0, data["attended"])
        total.insert(0, data["total"])

        update_percentage(
            data["attended"],
            data["total"]
        )

    def update_percentage(a, t):

        if t == 0:

            percentage.config(
                text="Attendance: 0.00%",
                fg=TEXT
            )

        else:

            p = (a / t) * 100

            percentage.config(
                text=f"Attendance: {p:.2f}%",
                fg=GREEN if p >= 75 else RED
            )

    def update():

        selected = subject_list.curselection()

        if not selected:
            messagebox.showwarning(
                "Select Subject",
                "Please select a subject."
            )
            return

        try:

            a = int(attended.get())
            t = int(total.get())

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter numbers."
            )

            return

        if a > t:

            messagebox.showerror(
                "Invalid Input",
                "Attended classes cannot exceed total classes."
            )

            return

        subject = subject_list.get(selected[0])

        attendance_data[subject] = {
            "attended": a,
            "total": t
        }

        save_json(
            ATTENDANCE_FILE,
            attendance_data
        )

        update_percentage(a, t)

        messagebox.showinfo(
            "Updated",
            "Attendance updated successfully."
        )

    subject_list.bind(
        "<<ListboxSelect>>",
        select_subject
    )

    tk.Button(
        right,
        text="UPDATE ATTENDANCE",
        command=update,
        bg=PURPLE,
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        height=2
    ).pack(fill="x", pady=10)


# ============================================================
# ASSIGNMENTS
# ============================================================

def open_assignments():

    window = tk.Toplevel(root)
    window.title("Assignment Manager")
    window.geometry("800x600")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="ASSIGNMENT MANAGER",
        bg=LIGHT_PURPLE,
        fg=TEXT,
        font=("Arial", 20, "bold")
    ).pack(fill="x", pady=15, ipady=10)

    # Load existing assignments
    data = load_json(ASSIGNMENT_FILE, [])

    # Make sure data is a list
    if not isinstance(data, list):
        data = []

    assignments = data

    frame = tk.Frame(
        window,
        bg=CARD
    )
    frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=20
    )

    # --------------------------------------------------------
    # SUBJECT
    # --------------------------------------------------------

    tk.Label(
        frame,
        text="Subject:",
        bg=CARD,
        fg=TEXT,
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="w"
    )

    subject_entry = tk.Entry(
        frame,
        width=35,
        font=("Arial", 11)
    )

    subject_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=10,
        ipady=5
    )

    # --------------------------------------------------------
    # ASSIGNMENT
    # --------------------------------------------------------

    tk.Label(
        frame,
        text="Assignment:",
        bg=CARD,
        fg=TEXT,
        font=("Arial", 11, "bold")
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10,
        sticky="w"
    )

    assignment_entry = tk.Entry(
        frame,
        width=35,
        font=("Arial", 11)
    )

    assignment_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=10,
        ipady=5
    )

    # --------------------------------------------------------
    # DUE DATE
    # --------------------------------------------------------

    tk.Label(
        frame,
        text="Due Date:",
        bg=CARD,
        fg=TEXT,
        font=("Arial", 11, "bold")
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=10,
        sticky="w"
    )

    date_entry = tk.Entry(
        frame,
        width=35,
        font=("Arial", 11)
    )

    date_entry.grid(
        row=2,
        column=1,
        padx=10,
        pady=10,
        ipady=5
    )

    # --------------------------------------------------------
    # ASSIGNMENT LIST
    # --------------------------------------------------------

    list_frame = tk.Frame(
        frame,
        bg=CARD
    )

    list_frame.grid(
        row=4,
        column=0,
        columnspan=2,
        padx=10,
        pady=15,
        sticky="nsew"
    )

    scrollbar = tk.Scrollbar(
        list_frame
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    assignment_list = tk.Listbox(
        list_frame,
        width=75,
        height=12,
        font=("Arial", 11),
        yscrollcommand=scrollbar.set
    )

    assignment_list.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=assignment_list.yview
    )

    # --------------------------------------------------------
    # REFRESH LIST
    # --------------------------------------------------------

    def refresh_assignments():

        assignment_list.delete(
            0,
            tk.END
        )

        for number, item in enumerate(assignments, start=1):

            subject = item.get("subject", "")
            task = item.get("task", "")
            date = item.get("date", "")

            assignment_list.insert(
                tk.END,
                f"{number}. {subject} | {task} | Due: {date}"
            )

    # --------------------------------------------------------
    # ADD ASSIGNMENT
    # --------------------------------------------------------

    def add_assignment():

        subject = subject_entry.get().strip()
        task = assignment_entry.get().strip()
        due_date = date_entry.get().strip()

        if subject == "":
            messagebox.showwarning(
                "Missing Subject",
                "Please enter the subject."
            )
            subject_entry.focus()
            return

        if task == "":
            messagebox.showwarning(
                "Missing Assignment",
                "Please enter the assignment."
            )
            assignment_entry.focus()
            return

        if due_date == "":
            messagebox.showwarning(
                "Missing Due Date",
                "Please enter the due date."
            )
            date_entry.focus()
            return

        new_assignment = {
            "subject": subject,
            "task": task,
            "date": due_date
        }

        assignments.append(
            new_assignment
        )

        # Save immediately
        save_json(
            ASSIGNMENT_FILE,
            assignments
        )

        # Update interface immediately
        refresh_assignments()

        # Clear input boxes
        subject_entry.delete(
            0,
            tk.END
        )

        assignment_entry.delete(
            0,
            tk.END
        )

        date_entry.delete(
            0,
            tk.END
        )

        subject_entry.focus()

        messagebox.showinfo(
            "Assignment Added",
            "Assignment added successfully!"
        )

    # --------------------------------------------------------
    # DELETE ASSIGNMENT
    # --------------------------------------------------------

    def delete_assignment():

        selected = assignment_list.curselection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select an assignment to delete."
            )

            return

        index = selected[0]

        del assignments[index]

        save_json(
            ASSIGNMENT_FILE,
            assignments
        )

        refresh_assignments()

    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    button_frame = tk.Frame(
        frame,
        bg=CARD
    )

    button_frame.grid(
        row=3,
        column=0,
        columnspan=2,
        pady=10
    )

    tk.Button(
        button_frame,
        text="ADD ASSIGNMENT",
        command=add_assignment,
        bg=BLUE,
        fg="white",
        font=("Arial", 11, "bold"),
        width=20,
        height=2,
        relief="flat",
        cursor="hand2"
    ).pack(
        side="left",
        padx=10
    )

    tk.Button(
        button_frame,
        text="DELETE SELECTED",
        command=delete_assignment,
        bg=RED,
        fg="white",
        font=("Arial", 11, "bold"),
        width=20,
        height=2,
        relief="flat",
        cursor="hand2"
    ).pack(
        side="left",
        padx=10
    )

    frame.columnconfigure(
        1,
        weight=1
    )

    frame.rowconfigure(
        4,
        weight=1
    )

    # Display existing assignments
    refresh_assignments()

# ============================================================
# CGPA CALCULATOR
# ============================================================

def open_cgpa():

    window = tk.Toplevel(root)

    window.title("CGPA Calculator")
    window.geometry("650x550")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="CGPA CALCULATOR",
        bg=LIGHT_PURPLE,
        fg=TEXT,
        font=("Arial", 20, "bold")
    ).pack(
        fill="x",
        pady=15,
        ipady=10
    )

    frame = tk.Frame(
        window,
        bg=CARD
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    tk.Label(
        frame,
        text="Enter credits and grade points for your 4 subjects",
        bg=CARD,
        fg=GRAY,
        font=("Arial", 11)
    ).pack(
        pady=10
    )

    # --------------------------------------------------------
    # TABLE HEADER
    # --------------------------------------------------------

    header = tk.Frame(
        frame,
        bg=CARD
    )

    header.pack(
        pady=5
    )

    tk.Label(
        header,
        text="Subject",
        bg=CARD,
        fg=TEXT,
        font=("Arial", 10, "bold"),
        width=15
    ).grid(
        row=0,
        column=0
    )

    tk.Label(
        header,
        text="Credits",
        bg=CARD,
        fg=TEXT,
        font=("Arial", 10, "bold"),
        width=12
    ).grid(
        row=0,
        column=1
    )

    tk.Label(
        header,
        text="Grade Point",
        bg=CARD,
        fg=TEXT,
        font=("Arial", 10, "bold"),
        width=12
    ).grid(
        row=0,
        column=2
    )

    # --------------------------------------------------------
    # EXACTLY 4 SUBJECTS
    # --------------------------------------------------------

    subject_names = [
        "Subject 1",
        "Subject 2",
        "Subject 3",
        "Subject 4"
    ]

    rows = []

    for i in range(4):

        row = tk.Frame(
            frame,
            bg=CARD
        )

        row.pack(
            pady=6
        )

        tk.Label(
            row,
            text=subject_names[i],
            bg=CARD,
            fg=TEXT,
            width=15
        ).grid(
            row=0,
            column=0
        )

        credit_entry = tk.Entry(
            row,
            width=12,
            font=("Arial", 11)
        )

        credit_entry.grid(
            row=0,
            column=1,
            padx=5,
            ipady=5
        )

        grade_entry = tk.Entry(
            row,
            width=12,
            font=("Arial", 11)
        )

        grade_entry.grid(
            row=0,
            column=2,
            padx=5,
            ipady=5
        )

        rows.append(
            (credit_entry, grade_entry)
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    result = tk.Label(
        frame,
        text="CGPA: --",
        bg="#EEF5FF",
        fg=TEXT,
        font=("Arial", 18, "bold"),
        pady=15
    )

    result.pack(
        fill="x",
        pady=20
    )

    # --------------------------------------------------------
    # CALCULATE
    # --------------------------------------------------------

    def calculate():

        total_points = 0
        total_credits = 0

        try:

            for credit_entry, grade_entry in rows:

                credit_text = credit_entry.get().strip()
                grade_text = grade_entry.get().strip()

                # Ignore completely empty rows
                if credit_text == "" and grade_text == "":
                    continue

                # Both values must be entered
                if credit_text == "" or grade_text == "":

                    messagebox.showwarning(
                        "Incomplete Subject",
                        "Please enter both credits and grade point."
                    )

                    return

                credits = float(
                    credit_text
                )

                grade_point = float(
                    grade_text
                )

                if credits <= 0:

                    messagebox.showerror(
                        "Invalid Credits",
                        "Credits must be greater than 0."
                    )

                    return

                if grade_point < 0 or grade_point > 10:

                    messagebox.showerror(
                        "Invalid Grade Point",
                        "Grade point must be between 0 and 10."
                    )

                    return

                total_points += (
                    credits * grade_point
                )

                total_credits += credits

            if total_credits == 0:

                messagebox.showwarning(
                    "No Data",
                    "Please enter your subject details."
                )

                return

            cgpa = (
                total_points /
                total_credits
            )

            result.config(
                text=f"CGPA: {cgpa:.2f}"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Credits and grade points must be numbers."
            )

    tk.Button(
        frame,
        text="CALCULATE CGPA",
        command=calculate,
        bg=PURPLE,
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        height=2,
        cursor="hand2"
    ).pack(
        fill="x"
    )

# ============================================================
# STUDY PLANNER
# ============================================================

def open_planner():

    window = tk.Toplevel(root)

    window.title("Study Planner")
    window.geometry("700x550")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="STUDY PLANNER",
        bg=LIGHT_PURPLE,
        fg=TEXT,
        font=("Arial", 20, "bold")
    ).pack(fill="x", pady=15, ipady=10)

    study_plan = load_json(
        PLANNER_FILE,
        []
    )

    frame = tk.Frame(window, bg=CARD)
    frame.pack(fill="both", expand=True, padx=25, pady=20)

    tk.Label(
        frame,
        text="Date:",
        bg=CARD
    ).grid(row=0, column=0, padx=10, pady=10)

    date_entry = tk.Entry(frame, width=30)
    date_entry.grid(row=0, column=1)

    tk.Label(
        frame,
        text="Study Task:",
        bg=CARD
    ).grid(row=1, column=0, padx=10, pady=10)

    task_entry = tk.Entry(frame, width=30)
    task_entry.grid(row=1, column=1)

    listbox = tk.Listbox(
        frame,
        width=65,
        height=14
    )

    listbox.grid(
        row=3,
        column=0,
        columnspan=2,
        pady=20
    )

    def refresh():

        listbox.delete(0, tk.END)

        for item in study_plan:

            listbox.insert(
                tk.END,
                f"{item['date']}  |  {item['task']}"
            )

    def add():

        date = date_entry.get().strip()
        task = task_entry.get().strip()

        if not date or not task:

            messagebox.showwarning(
                "Missing Information",
                "Enter date and study task."
            )

            return

        study_plan.append({
            "date": date,
            "task": task
        })

        save_json(
            PLANNER_FILE,
            study_plan
        )

        date_entry.delete(0, tk.END)
        task_entry.delete(0, tk.END)

        refresh()

    def delete():

        selected = listbox.curselection()

        if selected:

            study_plan.pop(selected[0])

            save_json(
                PLANNER_FILE,
                study_plan
            )

            refresh()

    tk.Button(
        frame,
        text="ADD STUDY TASK",
        command=add,
        bg=GREEN,
        fg="white",
        width=20,
        relief="flat"
    ).grid(row=2, column=1, pady=10)

    tk.Button(
        frame,
        text="DELETE TASK",
        command=delete,
        bg=RED,
        fg="white",
        width=20,
        relief="flat"
    ).grid(row=4, column=1)

    refresh()


# ============================================================
# NOTICE BOARD
# ============================================================

def open_notice_board():

    window = tk.Toplevel(root)
    window.title("Notice Board")
    window.geometry("800x600")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="NOTICE BOARD",
        bg=LIGHT_PURPLE,
        fg=TEXT,
        font=("Arial", 20, "bold")
    ).pack(
        fill="x",
        pady=15,
        ipady=10
    )

    # --------------------------------------------------------
    # LOAD NOTICES
    # --------------------------------------------------------

    data = load_json(
        NOTICE_FILE,
        []
    )

    # Make sure notices is a list
    if not isinstance(data, list):
        data = []

    notices = data

    # --------------------------------------------------------
    # MAIN FRAME
    # --------------------------------------------------------

    frame = tk.Frame(
        window,
        bg=CARD
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=20
    )

    # --------------------------------------------------------
    # NOTICE INPUT
    # --------------------------------------------------------

    tk.Label(
        frame,
        text="Enter Notice:",
        bg=CARD,
        fg=TEXT,
        font=("Arial", 11, "bold")
    ).pack(
        anchor="w",
        padx=10,
        pady=(5, 5)
    )

    notice_entry = tk.Entry(
        frame,
        font=("Arial", 11)
    )

    notice_entry.pack(
        fill="x",
        padx=10,
        ipady=8
    )

    # --------------------------------------------------------
    # BUTTON FRAME
    # --------------------------------------------------------

    button_frame = tk.Frame(
        frame,
        bg=CARD
    )

    button_frame.pack(
        pady=15
    )

    # --------------------------------------------------------
    # NOTICE LIST
    # --------------------------------------------------------

    list_frame = tk.Frame(
        frame,
        bg=CARD
    )

    list_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    scrollbar = tk.Scrollbar(
        list_frame
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    notice_list = tk.Listbox(
        list_frame,
        font=("Arial", 11),
        height=15,
        selectmode=tk.SINGLE,
        yscrollcommand=scrollbar.set
    )

    notice_list.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=notice_list.yview
    )

    # --------------------------------------------------------
    # REFRESH NOTICE LIST
    # --------------------------------------------------------

    def refresh_notices():

        notice_list.delete(
            0,
            tk.END
        )

        for number, notice in enumerate(
            notices,
            start=1
        ):

            notice_list.insert(
                tk.END,
                f"{number}. {notice}"
            )

    # --------------------------------------------------------
    # ADD NOTICE
    # --------------------------------------------------------

    def add_notice():

        notice = notice_entry.get().strip()

        if notice == "":

            messagebox.showwarning(
                "Empty Notice",
                "Please enter a notice first."
            )

            notice_entry.focus()

            return

        # Add notice to list
        notices.append(
            notice
        )

        # Save notice
        save_json(
            NOTICE_FILE,
            notices
        )

        # Immediately update interface
        refresh_notices()

        # Clear input box
        notice_entry.delete(
            0,
            tk.END
        )

        notice_entry.focus()

        messagebox.showinfo(
            "Notice Added",
            "Notice added successfully!"
        )

    # --------------------------------------------------------
    # DELETE NOTICE
    # --------------------------------------------------------

    def delete_notice():

        selected = notice_list.curselection()

        if not selected:

            messagebox.showwarning(
                "No Notice Selected",
                "Please select a notice to delete."
            )

            return

        index = selected[0]

        notices.pop(index)

        save_json(
            NOTICE_FILE,
            notices
        )

        refresh_notices()

    # --------------------------------------------------------
    # ADD BUTTON
    # --------------------------------------------------------

    tk.Button(
        button_frame,
        text="ADD NOTICE",
        command=add_notice,
        bg=BLUE,
        fg="white",
        font=("Arial", 11, "bold"),
        width=20,
        height=2,
        relief="flat",
        cursor="hand2"
    ).pack(
        side="left",
        padx=10
    )

    # --------------------------------------------------------
    # DELETE BUTTON
    # --------------------------------------------------------

    tk.Button(
        button_frame,
        text="DELETE NOTICE",
        command=delete_notice,
        bg=RED,
        fg="white",
        font=("Arial", 11, "bold"),
        width=20,
        height=2,
        relief="flat",
        cursor="hand2"
    ).pack(
        side="left",
        padx=10
    )

    # --------------------------------------------------------
    # INITIAL DISPLAY
    # --------------------------------------------------------

    refresh_notices()

    notice_entry.focus()
# ============================================================
# DASHBOARD
# ============================================================

header = tk.Frame(
    root,
    bg=LIGHT_PURPLE,
    height=75
)

header.pack(
    fill="x",
    padx=15,
    pady=(15, 5)
)

header.pack_propagate(False)

tk.Label(
    header,
    text="Student Management System",
    bg=LIGHT_PURPLE,
    fg=TEXT,
    font=("Arial", 23, "bold")
).pack(
    side="left",
    padx=25,
    pady=18
)


# ============================================================
# DASHBOARD CONTENT
# ============================================================

dashboard = tk.Frame(
    root,
    bg=BG
)

dashboard.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=25
)


tk.Label(
    dashboard,
    text="Dashboard",
    bg=BG,
    fg=TEXT,
    font=("Arial", 18, "bold")
).pack(
    anchor="w",
    pady=(0, 20)
)


# ============================================================
# MODULE BUTTONS
# ============================================================

buttons = [
    ("Student Profile", open_profile, BLUE),
    ("Attendance", open_attendance, PURPLE),
    ("Assignments", open_assignments, ORANGE),
    ("CGPA Calculator", open_cgpa, GREEN),
    ("Study Planner", open_planner, BLUE),
    ("Notice Board", open_notice_board, RED)
]


button_frame = tk.Frame(
    dashboard,
    bg=BG
)

button_frame.pack(
    fill="both",
    expand=True
)


for i, (text, command, color) in enumerate(buttons):

    card = tk.Frame(
        button_frame,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    row = i // 3
    column = i % 3

    card.grid(
        row=row,
        column=column,
        padx=12,
        pady=12,
        sticky="nsew"
    )

    tk.Label(
        card,
        text=text,
        bg=CARD,
        fg=TEXT,
        font=("Arial", 15, "bold")
    ).pack(
        pady=(35, 15)
    )

    tk.Button(
        card,
        text="OPEN",
        command=command,
        bg=color,
        fg="white",
        font=("Arial", 11, "bold"),
        width=18,
        height=2,
        relief="flat",
        cursor="hand2"
    ).pack(
        pady=(0, 35)
    )


for i in range(3):
    button_frame.columnconfigure(i, weight=1)

for i in range(2):
    button_frame.rowconfigure(i, weight=1)


# ============================================================
# FOOTER
# ============================================================

tk.Label(
    root,
    text="Student Management System • Python Tkinter",
    bg=BG,
    fg=GRAY,
    font=("Arial", 9)
).pack(
    pady=(0, 10)
)


# ============================================================
# RUN
# ============================================================

root.mainloop()
 
