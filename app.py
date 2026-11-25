
from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import date

app = Flask(__name__)

STUDENT_FILE = "students.csv"
ATTENDANCE_FILE = "attendance.csv"


def initialize_files():
    if not os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "w", newline="") as f:
            csv.writer(f).writerow(
                ["id", "name", "department", "semester"]
            )

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            csv.writer(f).writerow(
                ["student_id", "date", "status"]
            )


def load_students():
    with open(STUDENT_FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


def load_attendance():
    with open(ATTENDANCE_FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/dashboard")
def dashboard():
    students = load_students()
    attendance = load_attendance()

    today = date.today().isoformat()

    today_records = [
        r for r in attendance if r["date"] == today
    ]

    present = sum(
        1 for r in today_records if r["status"] == "Present"
    )

    absent = sum(
        1 for r in today_records if r["status"] == "Absent"
    )

    total = len(today_records)

    percentage = round((present / total) * 100, 2) if total else 0

    return jsonify({
        "total_students": len(students),
        "present": present,
        "absent": absent,
        "attendance_percentage": percentage,
        "today": today
    })


@app.route("/api/students", methods=["GET", "POST"])
def students_api():

    if request.method == "GET":
        return jsonify(load_students())

    data = request.get_json()

    student_id = str(data.get("id", "")).strip()
    name = str(data.get("name", "")).strip()
    department = str(data.get("department", "")).strip()
    semester = str(data.get("semester", "")).strip()

    if not all([student_id, name, department, semester]):
        return jsonify({"error": "All fields are required"}), 400

    if not semester.isdigit() or int(semester) < 1:
        return jsonify({"error": "Invalid semester"}), 400

    if any(s["id"] == student_id for s in load_students()):
        return jsonify({"error": "Student ID already exists"}), 400

    with open(STUDENT_FILE, "a", newline="") as f:
        csv.writer(f).writerow([
            student_id, name, department, semester
        ])

    return jsonify({"message": "Student added successfully"}), 201

# ==========================================
# EDIT AND DELETE STUDENT
# ==========================================

@app.route("/api/students/<student_id>", methods=["PUT", "DELETE"])
def manage_student(student_id):

    students = load_students()

    # Find the selected student
    selected_student = next(
        (s for s in students if s["id"] == student_id),
        None
    )

    if selected_student is None:
        return jsonify({"error": "Student not found"}), 404

    # ---------------- EDIT STUDENT ----------------
    if request.method == "PUT":

        data = request.get_json(silent=True) or {}

        name = str(data.get("name", "")).strip()
        department = str(data.get("department", "")).strip()
        semester = str(data.get("semester", "")).strip()

        if not all([name, department, semester]):
            return jsonify({"error": "All fields are required"}), 400

        if not semester.isdigit() or int(semester) < 1:
            return jsonify({"error": "Invalid semester"}), 400

        # Update the selected student's details
        selected_student["name"] = name
        selected_student["department"] = department
        selected_student["semester"] = semester

        # Save all students back to the CSV file
        with open(STUDENT_FILE, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "name", "department", "semester"]
            )
            writer.writeheader()
            writer.writerows(students)

        return jsonify({"message": "Student updated successfully"})

    # ---------------- DELETE STUDENT ----------------
    if request.method == "DELETE":

        # Remove the student from the student list
        updated_students = [
            s for s in students if s["id"] != student_id
        ]

        with open(STUDENT_FILE, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "name", "department", "semester"]
            )
            writer.writeheader()
            writer.writerows(updated_students)

        # Remove this student's attendance records too
        attendance = load_attendance()

        updated_attendance = [
            r for r in attendance
            if r["student_id"] != student_id
        ]

        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["student_id", "date", "status"]
            )
            writer.writeheader()
            writer.writerows(updated_attendance)

        return jsonify({"message": "Student deleted successfully"})

@app.route("/api/attendance", methods=["GET", "POST"])
def attendance_api():

    if request.method == "GET":
        students = {
            s["id"]: s["name"] for s in load_students()
        }

        records = load_attendance()

        for record in records:
            record["student_name"] = students.get(
                record["student_id"], "Unknown"
            )

        return jsonify(records)

    data = request.get_json()

    student_id = str(data.get("student_id", "")).strip()
    status = str(data.get("status", "")).strip()

    students = load_students()

    if not any(s["id"] == student_id for s in students):
        return jsonify({"error": "Student not found"}), 404

    if status not in ["Present", "Absent"]:
        return jsonify({"error": "Invalid attendance status"}), 400

    today = date.today().isoformat()

    attendance = load_attendance()

    if any(
        r["student_id"] == student_id and r["date"] == today
        for r in attendance
    ):
        return jsonify({
            "error": "Attendance already marked for today"
        }), 400

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        csv.writer(f).writerow([
            student_id, today, status
        ])

    return jsonify({"message": "Attendance marked successfully"}), 201


@app.route("/api/report")
def report_api():

    students = load_students()
    attendance = load_attendance()

    report = []

    for student in students:
        records = [
            r for r in attendance
            if r["student_id"] == student["id"]
        ]

        total = len(records)

        present = sum(
            1 for r in records if r["status"] == "Present"
        )

        percentage = round(
            (present / total) * 100, 2
        ) if total else 0

        report.append({
            "id": student["id"],
            "name": student["name"],
            "present": present,
            "total": total,
            "percentage": percentage
        })

    return jsonify(report)


@app.route("/api/search")
def search_api():

    student_id = request.args.get("id", "").strip()

    for student in load_students():
        if student["id"] == student_id:
            return jsonify(student)

    return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    initialize_files()
    app.run(debug=True)
