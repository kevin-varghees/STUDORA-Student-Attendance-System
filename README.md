# STUDORA – Student Attendance Management System

STUDORA is a web-based Student Attendance Management System developed using Python and Flask. It helps manage student details, record daily attendance, search student information, and generate attendance reports through a simple and user-friendly interface.

## Features

- Dashboard with student and attendance statistics
- Add new student records
- View all registered students
- Edit existing student details
- Delete student records
- Mark students as Present or Absent
- View attendance records
- Generate attendance percentage reports
- Search students using their ID
- CSV-based data storage

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- CSV Files

## Project Structure

```text
STUDORA-Student-Attendance-System/
│
├── app.py
├── main.py
├── requirements.txt
├── students.csv
├── attendance.csv
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/STUDORA-Student-Attendance-System.git
```

### 2. Open the project folder

```bash
cd STUDORA-Student-Attendance-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in browser

Visit:

http://127.0.0.1:5000

## Data Storage

Student information and attendance records are stored in CSV files:

- `students.csv` – Stores student details.
- `attendance.csv` – Stores attendance records.

## Project Purpose

This project was developed as an academic Python project to demonstrate Python programming, web development, backend integration, and file-based data management.

## Future Enhancements

- Database integration
- User authentication
- Attendance notifications
- PDF and Excel report generation
- Mobile
