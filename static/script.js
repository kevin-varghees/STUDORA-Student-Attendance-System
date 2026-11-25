const API = "/api";

const $ = (id) => document.getElementById(id);

// ==========================================
// NAVIGATION
// ==========================================

function showPage(page) {
  document.querySelectorAll(".page").forEach((section) => {
    section.classList.remove("active");
  });

  document.querySelectorAll(".nav-btn").forEach((button) => {
    button.classList.toggle("active", button.dataset.page === page);
  });

  const selectedPage = $(page);

  if (!selectedPage) return;

  selectedPage.classList.add("active");

  const titles = {
    dashboard: "Dashboard",
    students: "Student Management",
    mark: "Mark Attendance",
    records: "Attendance Records",
    report: "Attendance Report",
    search: "Search Student",
  };

  $("page-title").textContent = titles[page] || "STUDORA";

  if (page === "dashboard") loadDashboard();
  if (page === "students") loadStudents();
  if (page === "records") loadRecords();
  if (page === "report") loadReport();
}

document.querySelectorAll(".nav-btn").forEach((button) => {
  button.addEventListener("click", () => {
    showPage(button.dataset.page);
  });
});

// ==========================================
// NOTIFICATIONS
// ==========================================

function notify(message) {
  const toast = $("toast");

  if (!toast) {
    alert(message);
    return;
  }

  toast.textContent = message;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

// ==========================================
// API HELPER
// ==========================================

async function apiRequest(url, options = {}) {
  const response = await fetch(API + url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong");
  }

  return data;
}

// ==========================================
// ESCAPE HTML
// ==========================================

function escapeHTML(value) {
  return String(value).replace(
    /[&<>"']/g,
    (char) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      })[char],
  );
}

// ==========================================
// DASHBOARD
// ==========================================

async function loadDashboard() {
  try {
    const data = await apiRequest("/dashboard");

    $("total-students").textContent = data.total_students;
    $("present-count").textContent = data.present;
    $("absent-count").textContent = data.absent;
    $("attendance-rate").textContent = data.attendance_percentage + "%";
  } catch (error) {
    notify(error.message);
  }
}

// ==========================================
// LOAD STUDENTS
// ==========================================

async function loadStudents() {
  try {
    const students = await apiRequest("/students");

    $("students-table").innerHTML = students.length
      ? students
          .map(
            (s) => `
                <tr>
                    <td>${escapeHTML(s.id)}</td>
                    <td>${escapeHTML(s.name)}</td>
                    <td>${escapeHTML(s.department)}</td>
                    <td>${escapeHTML(s.semester)}</td>
                    <td>
                        <div class="action-buttons">
                            <button
                                class="edit-btn"
                                data-action="edit"
                                data-id="${escapeHTML(s.id)}">
                                Edit
                            </button>

                            <button
                                class="delete-btn"
                                data-action="delete"
                                data-id="${escapeHTML(s.id)}">
                                Delete
                            </button>
                        </div>
                    </td>
                </tr>
            `,
          )
          .join("")
      : `<tr><td colspan="5">No students found.</td></tr>`;
  } catch (error) {
    notify(error.message);
  }
}

// ==========================================
// ADD STUDENT
// ==========================================

$("student-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const student = {
    id: $("student-id").value.trim(),
    name: $("student-name").value.trim(),
    department: $("department").value.trim(),
    semester: $("semester").value.trim(),
  };

  try {
    const result = await apiRequest("/students", {
      method: "POST",
      body: JSON.stringify(student),
    });

    notify(result.message);
    $("student-form").reset();

    await loadStudents();
    await loadDashboard();
  } catch (error) {
    notify(error.message);
  }
});

// ==========================================
// EDIT AND DELETE STUDENT
// ==========================================

let editingStudentId = null;

// Handle Edit and Delete button clicks
$("students-table").addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-action]");

  if (!button) return;

  const studentId = button.dataset.id;

  // EDIT STUDENT
  if (button.dataset.action === "edit") {
    try {
      const students = await apiRequest("/students");

      const student = students.find((s) => String(s.id) === String(studentId));

      if (!student) {
        notify("Student not found");
        return;
      }

      editingStudentId = studentId;

      $("edit-student-id").value = student.id;
      $("edit-student-name").value = student.name;
      $("edit-department").value = student.department;
      $("edit-semester").value = student.semester;

      $("edit-student-panel").hidden = false;

      $("edit-student-panel").scrollIntoView({
        behavior: "smooth",
      });
    } catch (error) {
      notify(error.message);
    }
  }

  // DELETE STUDENT
  if (button.dataset.action === "delete") {
    const confirmed = confirm(
      `Are you sure you want to delete student ${studentId}? This will also delete their attendance history.`,
    );

    if (!confirmed) return;

    try {
      const result = await apiRequest(
        `/students/${encodeURIComponent(studentId)}`,
        {
          method: "DELETE",
        },
      );

      notify(result.message);

      await loadStudents();
      await loadDashboard();
      await loadReport();
      await loadRecords();
    } catch (error) {
      notify(error.message);
    }
  }
});

// SAVE EDITED STUDENT
$("edit-student-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!editingStudentId) return;

  const updatedStudent = {
    name: $("edit-student-name").value.trim(),
    department: $("edit-department").value.trim(),
    semester: $("edit-semester").value.trim(),
  };

  if (
    !updatedStudent.name ||
    !updatedStudent.department ||
    !updatedStudent.semester
  ) {
    notify("Please fill in all fields");
    return;
  }

  try {
    const result = await apiRequest(
      `/students/${encodeURIComponent(editingStudentId)}`,
      {
        method: "PUT",
        body: JSON.stringify(updatedStudent),
      },
    );

    notify(result.message);

    $("edit-student-form").reset();
    $("edit-student-panel").hidden = true;

    editingStudentId = null;

    await loadStudents();
    await loadDashboard();
    await loadReport();
    await loadRecords();
  } catch (error) {
    notify(error.message);
  }
});

// CANCEL EDIT
$("cancel-edit").addEventListener("click", () => {
  $("edit-student-form").reset();
  $("edit-student-panel").hidden = true;

  editingStudentId = null;
});

// ==========================================
// MARK ATTENDANCE
// ==========================================

$("attendance-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const record = {
    student_id: $("attendance-id").value.trim(),
    status: $("attendance-status").value,
  };

  try {
    const result = await apiRequest("/attendance", {
      method: "POST",
      body: JSON.stringify(record),
    });

    notify(result.message);
    $("attendance-form").reset();

    await loadDashboard();
  } catch (error) {
    notify(error.message);
  }
});

// ==========================================
// ATTENDANCE RECORDS
// ==========================================

async function loadRecords() {
  try {
    const records = await apiRequest("/attendance");

    $("records-table").innerHTML = records.length
      ? records
          .map(
            (r) => `
                <tr>
                    <td>${escapeHTML(r.student_id)}</td>
                    <td>${escapeHTML(r.student_name)}</td>
                    <td>${escapeHTML(r.date)}</td>
                    <td>
                        <span class="status ${escapeHTML(r.status)}">
                            ${escapeHTML(r.status)}
                        </span>
                    </td>
                </tr>
            `,
          )
          .join("")
      : `<tr><td colspan="4">No attendance records found.</td></tr>`;
  } catch (error) {
    notify(error.message);
  }
}

// ==========================================
// ATTENDANCE REPORT
// ==========================================

async function loadReport() {
  try {
    const report = await apiRequest("/report");

    $("report-table").innerHTML = report.length
      ? report
          .map(
            (r) => `
                <tr>
                    <td>${escapeHTML(r.id)}</td>
                    <td>${escapeHTML(r.name)}</td>
                    <td>${r.present}</td>
                    <td>${r.total}</td>
                    <td>${r.percentage}%</td>
                </tr>
            `,
          )
          .join("")
      : `<tr><td colspan="5">No students found.</td></tr>`;
  } catch (error) {
    notify(error.message);
  }
}

// ==========================================
// SEARCH STUDENT
// ==========================================

$("search-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const id = $("search-id").value.trim();

  try {
    const student = await apiRequest("/search?id=" + encodeURIComponent(id));

    $("search-result").innerHTML = `
            <h3>Student Found!</h3>
            <p><b>Student ID:</b> ${escapeHTML(student.id)}</p>
            <p><b>Name:</b> ${escapeHTML(student.name)}</p>
            <p><b>Department:</b> ${escapeHTML(student.department)}</p>
            <p><b>Semester:</b> ${escapeHTML(student.semester)}</p>
        `;
  } catch (error) {
    $("search-result").textContent = error.message;
  }
});

// ==========================================
// DISPLAY CURRENT DATE
// ==========================================

$("current-date").textContent = new Date().toLocaleDateString("en-IN", {
  day: "numeric",
  month: "short",
  year: "numeric",
});

// ==========================================
// INITIAL DASHBOARD
// ==========================================

loadDashboard();
