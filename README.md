# Day 5 – Project Architecture & Planning

This project starts from the Week 3 / Day 3 Flask repository and implements the Day 5 architecture and planning exercise.

Original source branch: `w8-d3`

## Features

- Role-based users: `admin`, `instructor`, `student`
- Student ↔ Course many-to-many relationship
- Profile picture upload
- Course enrollment API
- Student search
- Student pagination
- Git branching strategy and milestones
- Database schema documentation
- API specification

## Project structure

```text
day5_project/
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── student.py
│   │   └── course.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── students.py
│   │   ├── courses.py
│   │   ├── profile.py
│   │   └── api.py
│   ├── templates/
│   ├── extensions.py
│   └── __init__.py
├── docs/
│   ├── schema.dbml
│   └── api-spec.md
├── requirements.txt
├── run.py
├── seed.py
├── BRANCHING.md
└── README.md
```

## Requirements

Python 3.10+ recommended.

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

Initialize demo data:

```bash
python seed.py
```

Run:

```bash
python run.py
```

Open `http://127.0.0.1:5000/login`.

## Demo accounts

| Username | Password | Role |
|---|---|---|
| admin | admin123 | Admin |
| instructor | instructor123 | Instructor |
| student | student123 | Student |

The student demo account is linked to a Student record so the enrollment API can be tested immediately.

## Day 5 requirements → implementation

### 1. Role-based users

The `User` model now has a `role` field.

- Admin: can add students and courses.
- Instructor: can add students and courses.
- Student: can view data and enroll through the API.

### 2. Student-Course many-to-many

The `student_courses` association table connects students and courses.

A student can take many courses, and a course can contain many students.

### 3. Profile pictures

`/profile/` accepts PNG, JPG, JPEG, and GIF files.

Uploads are stored under `uploads/profile_pictures/`.

The upload size is limited to 2 MB.

### 4. Course enrollment API

```http
POST /api/courses/<course_id>/enroll
```

The logged-in student enrolls in the selected course.

Example:

```bash
curl -X POST http://127.0.0.1:5000/api/courses/1/enroll
```

The endpoint uses the existing Flask-Login session, so log in as the student first when testing with a browser.

### 5. Student search and pagination

```text
/students/?q=ali&page=1&per_page=10
```

- `q` searches name or email.
- `page` selects the page.
- `per_page` controls page size, capped at 50.

## API examples

### Enroll current student

```http
POST /api/courses/1/enroll
```

Success:

```json
{
  "message": "Enrollment successful.",
  "course_id": 1,
  "course_title": "Python Fundamentals",
  "student_id": 1
}
```

### List course students

```http
GET /api/courses/1/students
```

## Database schema

The schema is documented in `docs/schema.dbml`.

You can paste it into dbdiagram.io to visualize the ER diagram.

## Git branching strategy

- `main` = stable/release-ready code
- `dev` = integration branch
- `feature/*` = one feature per branch

Example:

```bash
git checkout main
git pull origin main

git checkout -b dev

git checkout -b feature/role-based-users
# implement + commit

git checkout dev
git merge --no-ff feature/role-based-users

git checkout -b feature/course-enrollment-api
# implement + commit

git checkout dev
git merge --no-ff feature/course-enrollment-api
```

See `BRANCHING.md` for milestones.

## Notes

This Day 5 version intentionally keeps the application's existing Flask structure while adding the requested architecture. For a production application, move the secret key and database URL into environment variables and add Flask-Migrate for database migrations.
