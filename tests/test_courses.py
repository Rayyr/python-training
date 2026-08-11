from app import db
from app.models.course import Course
from app.models.student import Student


def login(client, email="course-tests@example.com"):
    return client.post(
        "/signup",
        data={
            "name": "Course Tester",
            "email": email,
            "password": "secret123",
            "confirm_password": "secret123",
        },
    )


def add_course(app, code="CS101", name="Programming"):
    with app.app_context():
        course = Course(code=code, name=name, description="Description")
        db.session.add(course)
        db.session.commit()
        return course.id


def add_student(app, name="Student", email="student@example.com"):
    with app.app_context():
        student = Student(name=name, email=email)
        db.session.add(student)
        db.session.commit()
        return student.id


def test_courses_page_filter_and_pagination(client, app):
    login(client)
    for i in range(7):
        add_course(app, f"C{i:03d}", f"Course {i}")

    response = client.get("/courses")
    assert response.status_code == 200
    assert b"Course 0" in response.data

    response = client.get("/courses?q=Course 6")
    assert b"Course 6" in response.data
    assert b"Course 0" not in response.data

    response = client.get("/courses?page=2")
    assert response.status_code == 200


def test_create_course_success_duplicate_and_invalid(client, app):
    login(client)
    add_course(app, "CS101", "Programming")

    response = client.post(
        "/courses/new", data={"code": "cs101", "name": "Duplicate", "description": "x"}
    )
    assert b"already exists" in response.data

    response = client.post("/courses/new", data={"code": "", "name": "", "description": ""})
    assert response.status_code == 200

    response = client.post(
        "/courses/new",
        data={"code": "web201", "name": "Web Development", "description": "Flask"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"WEB201" in response.data


def test_edit_course_success_duplicate_and_invalid(client, app):
    login(client)
    course_id = add_course(app, "CS101", "Programming")
    add_course(app, "DB101", "Databases")

    response = client.post(
        f"/courses/{course_id}/edit",
        data={"code": "db101", "name": "Duplicate", "description": "x"},
    )
    assert b"already in use" in response.data

    response = client.post(
        f"/courses/{course_id}/edit",
        data={"code": "web101", "name": "Updated Course", "description": "Updated"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"WEB101" in response.data

    response = client.post(
        f"/courses/{course_id}/edit", data={"code": "", "name": "", "description": ""}
    )
    assert response.status_code == 200


def test_delete_course(client, app):
    login(client)
    course_id = add_course(app)
    response = client.post(f"/courses/{course_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Course, course_id) is None


def test_courses_api(client, app):
    login(client)
    add_course(app, "CS101", "Programming")
    response = client.get("/api/courses")
    assert response.status_code == 200
    assert response.json[0]["code"] == "CS101"


def test_enrollment_api_all_branches(client, app):
    login(client)
    course_id = add_course(app, "WEB101", "Web Development")
    student_id = add_student(app, "API Student", "api-student@example.com")

    response = client.get(f"/api/courses/{course_id}/enrollments")
    assert response.status_code == 200
    assert response.json == []

    response = client.post(f"/api/courses/{course_id}/enrollments", json={})
    assert response.status_code == 400
    assert b"student_id is required" in response.data

    response = client.post(f"/api/courses/{course_id}/enrollments", json={"student_id": student_id})
    assert response.status_code == 201
    assert response.json["message"] == "Enrollment created"

    response = client.post(f"/api/courses/{course_id}/enrollments", json={"student_id": student_id})
    assert response.status_code == 409
    assert b"Already enrolled" in response.data

    response = client.get(f"/api/courses/{course_id}/enrollments")
    assert response.status_code == 200
    assert response.json[0]["email"] == "api-student@example.com"


def test_course_and_enrollment_not_found(client):
    login(client)
    assert client.get("/courses/99999/edit").status_code == 404
    assert client.post("/courses/99999/delete").status_code == 404
    assert client.get("/api/courses/99999/enrollments").status_code == 404
