# Student Portal — Week 9 Final Project

A production-oriented Flask Student Portal implementing the Week 9 requirements:
database relationships, CRUD, filtering and pagination, REST API endpoints, profile-picture
uploads, Flask-WTF validation and CSRF protection, custom error pages, automated tests,
CI/CD, Bootstrap 5 frontend enhancements, dynamic API search, environment configuration,
and professional project documentation.

## Features

- User authentication: Sign Up, Login, Logout, secure password hashing, and protected routes
- Student CRUD
- Course CRUD
- Many-to-many Student/Course relationship through `Enrollment`
- Cascading deletes and unique enrollment constraints
- Student and course filtering
- Pagination
- Student profile-picture upload
- Flask-WTF forms, validation, CSRF protection and flash messages
- Custom 404 and 500 pages
- REST API for students, courses and enrollments
- JavaScript `fetch`-based dynamic student search
- Bootstrap 5 responsive UI
- Pytest test suite
- pytest-cov coverage enforcement
- Black and Flake8 checks
- GitHub Actions continuous testing
- CLI database seeding
- Environment variables with python-dotenv
- Deployment-ready Gunicorn command

## Setup

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set a secure `SECRET_KEY`.

Run the application:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## Seed sample data

```bash
flask --app seed.py seed
```

## Tests

```bash
pytest
```

Coverage:

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

Lint/format checks:

```bash
black --check .
flake8 .
```

## Authentication

- `GET/POST /signup` — create an account
- `GET/POST /login` — authenticate
- `POST /logout` — end the session
- Passwords are stored using secure Werkzeug password hashes.
- Student/course pages and APIs require login.
- CSRF protection is enabled for forms.

After seeding, demo credentials are:

```text
Email: admin@example.com
Password: admin123
```

Change or remove the demo account before production deployment.

## API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/students` | List/search students |
| GET | `/api/students/<id>` | Get one student |
| PUT | `/api/students/<id>` | Update a student |
| DELETE | `/api/students/<id>` | Delete a student |
| GET | `/api/courses` | List courses |
| GET | `/api/courses/<id>/enrollments` | List course enrollments |
| POST | `/api/courses/<id>/enrollments` | Create enrollment |

Example:

```bash
curl "http://127.0.0.1:5000/api/students?q=Alice"
```

## Database Schema

### Student

- `id` — primary key
- `name`
- `email` — unique
- `phone`
- `profile_picture`

### Course

- `id` — primary key
- `code` — unique
- `name`
- `description`

### Enrollment

- `id` — primary key
- `student_id` — foreign key to Student
- `course_id` — foreign key to Course
- `enrolled_at`
- unique `(student_id, course_id)`

Relationship:

```text
Student 1 ---- * Enrollment * ---- 1 Course
```

This provides the requested many-to-many Student/Course relationship.

## Folder Structure

```text
student_portal/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── student.py
│   │   ├── course.py
│   │   └── enrollment.py
│   ├── routes/
│   │   ├── students.py
│   │   ├── courses.py
│   │   └── auth.py
│   ├── templates/
│   ├── static/
│   └── forms/
├── tests/
│   ├── conftest.py
│   ├── test_students.py
│   ├── test_courses.py
│   └── test_auth.py
├── .github/workflows/python-app.yml
├── config.py
├── requirements.txt
├── run.py
├── seed.py
├── .env.example
└── README.md
```

## Deployment

For a Render/Railway-style deployment, configure environment variables:

- `SECRET_KEY`
- `DATABASE_URL`
- `UPLOAD_FOLDER` if required by the hosting environment

Gunicorn start command:

```bash
gunicorn run:app
```

For production, use a persistent database and persistent/object storage for uploaded images.

## Screenshots

Add screenshots of the running application here before final submission. Suggested screenshots:

1. Students list and pagination
2. Student profile with uploaded picture
3. Course list
4. Enrollment relationship
5. Dynamic student search
6. API response
7. GitHub Actions passing tests

## Deployment Link

Replace this section with the real deployed Render or Railway URL after deployment.

`https://YOUR-DEPLOYMENT-URL`

## Live Demo

Replace with the final live demo URL.

## GitHub Repository

Replace with the final GitHub repository URL.

## Notes

The deployment link, GitHub repository URL, and screenshots must be added after the project is actually pushed/deployed. These values cannot be generated locally.



## 🔮 Future Plans

The Student Portal can be further improved and expanded in future versions with the following features:

### 🔐 Authentication & Security
- Add a **Forgot Password / Password Reset** system.
- Allow students to **change their passwords**.
- Add stronger password requirements.
- Add login rate limiting and protection against repeated failed login attempts.
- Improve file-upload security and validation.

### 📊 Admin Dashboard
- Add a dedicated **Admin Dashboard**.
- Display statistics such as:
  - Total number of students.
  - Total number of courses.
  - Total number of enrollments.
  - Recently registered students.
  - Most popular courses.

### 🎓 Student Dashboard
- Create a personalized student dashboard.
- Display enrollment status.

### 📚 Course Management
- Add course capacity limits.
- Add course prerequisites.
- Add course start and end dates.
- Add course categories.

### 📝 Enrollment Management
- Add a complete enrollment management system for administrators.
- Add enrollment history.

### 🔔 Notifications
- Add notifications for students when:
  - They are removed from a course.
  - A new course is available.
- Add email notifications.

### 🌐 API Improvements
- Expand the REST API to support:
  - Students.
  - Courses.
  - Enrollments.
  - User information.
- Add API authentication and authorization.
- Add API documentation using **OpenAPI/Swagger/Postman**.

### 🧪 Testing & Code Quality
- Increase automated test coverage to **80–90% or higher**.
