
import csv
import os
from datetime import date

# ==========================================
# STUDENT ATTENDANCE MANAGEMENT SYSTEM
# ==========================================

STUDENT_FILE = "students.csv"
ATTENDANCE_FILE = "attendance.csv"


# Create CSV files automatically
def initialize_files():

    if not os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "department", "semester"])

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["student_id", "date", "status"])


# Read student records
def load_students():

    with open(STUDENT_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


# Read attendance records
def load_attendance():

    with open(ATTENDANCE_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


# Display main menu
def display_menu():

    print("\n==========================================")
    print("       STUDENT ATTENDANCE SYSTEM")
    print("==========================================")

    print("1. Add Student")
    print("2. View Students")
    print("3. Mark Attendance")
    print("4. View Attendance")
    print("5. Attendance Report")
    print("6. Search Student")
    print("7. Exit")

    print("==========================================")


# ==========================================
# 1. ADD STUDENT
# ==========================================

def add_student():

    print("\n----------- ADD STUDENT -----------")

    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty!")
        return

    students = load_students()

    for student in students:
        if student["id"] == student_id:
            print("Student ID already exists!")
            return

    name = input("Enter Student Name: ").strip()
    department = input("Enter Department: ").strip()
    semester = input("Enter Semester: ").strip()

    if not name or not department or not semester:
        print("All fields are required!")
        return

    if not semester.isdigit() or int(semester) < 1:
        print("Please enter a valid semester!")
        return

    with open(STUDENT_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            student_id,
            name,
            department,
            semester
        ])

    print("\nStudent added successfully!")


# ==========================================
# 2. VIEW STUDENTS
# ==========================================

def view_students():

    print("\n----------- STUDENT RECORDS -----------")

    students = load_students()

    if not students:
        print("No student records found!")
        return

    print("-" * 75)
    print(f"{'ID':<12}{'NAME':<20}{'DEPARTMENT':<25}{'SEMESTER':<10}")
    print("-" * 75)

    for student in students:

        print(
            f"{student['id']:<12}"
            f"{student['name']:<20}"
            f"{student['department']:<25}"
            f"{student['semester']:<10}"
        )

    print("-" * 75)


# ==========================================
# 3. MARK ATTENDANCE
# ==========================================

def mark_attendance():

    print("\n----------- MARK ATTENDANCE -----------")

    students = load_students()

    if not students:
        print("Please add students first!")
        return

    student_id = input("Enter Student ID: ").strip()

    selected_student = None

    for student in students:
        if student["id"] == student_id:
            selected_student = student
            break

    if selected_student is None:
        print("Student not found!")
        return

    print("Student Name:", selected_student["name"])

    today = date.today().isoformat()

    attendance = load_attendance()

    # Check whether attendance is already marked
    for record in attendance:

        if (record["student_id"] == student_id
                and record["date"] == today):

            print("Attendance already marked for today!")
            return

    print("\nSelect Attendance Status:")
    print("P - Present")
    print("A - Absent")

    status = input("Enter your choice: ").strip().upper()

    if status == "P":
        attendance_status = "Present"

    elif status == "A":
        attendance_status = "Absent"

    else:
        print("Invalid attendance choice!")
        return

    with open(ATTENDANCE_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            student_id,
            today,
            attendance_status
        ])

    print("\nAttendance marked successfully!")
    print("Student:", selected_student["name"])
    print("Date:", today)
    print("Status:", attendance_status)


# ==========================================
# 4. VIEW ATTENDANCE
# ==========================================

def view_attendance():

    print("\n----------- ATTENDANCE RECORDS -----------")

    attendance = load_attendance()

    if not attendance:
        print("No attendance records found!")
        return

    students = load_students()

    print("-" * 65)
    print(f"{'STUDENT ID':<15}{'STUDENT NAME':<20}{'DATE':<15}{'STATUS':<12}")
    print("-" * 65)

    for record in attendance:

        student_name = "Unknown"

        for student in students:
            if student["id"] == record["student_id"]:
                student_name = student["name"]
                break

        print(
            f"{record['student_id']:<15}"
            f"{student_name:<20}"
            f"{record['date']:<15}"
            f"{record['status']:<12}"
        )

    print("-" * 65)


# ==========================================
# 5. ATTENDANCE REPORT
# ==========================================

def attendance_report():

    print("\n----------- ATTENDANCE REPORT -----------")

    students = load_students()
    attendance = load_attendance()

    if not students:
        print("No student records found!")
        return

    print("-" * 75)
    print(f"{'ID':<12}{'NAME':<20}{'PRESENT':<12}{'TOTAL':<10}{'PERCENTAGE':<12}")
    print("-" * 75)

    for student in students:

        total = 0
        present = 0

        for record in attendance:

            if record["student_id"] == student["id"]:

                total += 1

                if record["status"] == "Present":
                    present += 1

        if total > 0:
            percentage = (present / total) * 100
        else:
            percentage = 0

        print(
            f"{student['id']:<12}"
            f"{student['name']:<20}"
            f"{present:<12}"
            f"{total:<10}"
            f"{percentage:.2f}%"
        )

    print("-" * 75)
    print("Note: Percentage is based on recorded attendance entries.")


# ==========================================
# 6. SEARCH STUDENT
# ==========================================

def search_student():

    print("\n----------- SEARCH STUDENT -----------")

    student_id = input("Enter Student ID to search: ").strip()

    students = load_students()

    for student in students:

        if student["id"] == student_id:

            print("\nStudent Found!")
            print("----------------------------")
            print("Student ID :", student["id"])
            print("Name       :", student["name"])
            print("Department :", student["department"])
            print("Semester   :", student["semester"])
            print("----------------------------")

            return

    print("Student not found!")


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():

    initialize_files()

    while True:

        display_menu()

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            mark_attendance()

        elif choice == "4":
            view_attendance()

        elif choice == "5":
            attendance_report()

        elif choice == "6":
            search_student()

        elif choice == "7":
            print("\nThank you for using Student Attendance System!")
            print("Program closed successfully.")
            break

        else:
            print("Invalid choice! Please enter a number from 1 to 7.")


# ==========================================
# START THE PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
