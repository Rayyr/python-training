# API Specification

Base URL:

```text
http://127.0.0.1:5000/api
```

Authentication uses the Flask-Login session.

## POST /courses/{course_id}/enroll

Enroll the currently authenticated student in a course.

### Authentication

Required.

### Authorization

The current user must have the `student` role and must be linked to a Student record.

### Request

```http
POST /api/courses/1/enroll
```

No JSON body is required.

### Responses

**201 Created**

```json
{
  "message": "Enrollment successful.",
  "course_id": 1,
  "course_title": "Python Fundamentals",
  "student_id": 1
}
```

**200 OK** if already enrolled.

**400 Bad Request** if the user is not linked to a Student record.

**403 Forbidden** if the current user is not a student.

**404 Not Found** if the course does not exist.

## GET /courses/{course_id}/students

Return all students enrolled in a course.

### Authentication

Required.

### Request

```http
GET /api/courses/1/students
```

### Response

```json
{
  "course": {
    "id": 1,
    "title": "Python Fundamentals"
  },
  "students": [
    {
      "id": 1,
      "name": "Demo Student",
      "email": "student@example.com"
    }
  ]
}
```

## Student web list

The student list is a web endpoint rather than a JSON API:

```text
GET /students/?q=<search>&page=<page>&per_page=<size>
```

Example:

```text
/students/?q=demo&page=1&per_page=10
```
