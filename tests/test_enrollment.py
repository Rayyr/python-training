from app.extensions import db
from app.models.course import Course
from app.models.student import Student


def login(client):
    client.post(
        "/register",
        data={
            "username": "tester",
            "password": "password123",
        },
    )

    client.post(
        "/login",
        data={
            "username": "tester",
            "password": "password123",
        },
    )


def create_student_and_course(app):
    with app.app_context():
        student = Student(
            name="Raya",
            email="raya@example.com",
        )

        course = Course(
            title="Python",
        )

        db.session.add(student)
        db.session.add(course)
        db.session.commit()

        return student.id, course.id


def test_enrollment_requires_login(client, app):
    student_id, course_id = create_student_and_course(app)

    response = client.post(
        "/api/enrollment/",
        json={
            "student_id": student_id,
            "course_id": course_id,
        },
    )

    assert response.status_code == 302


def test_enroll_student(client, app):
    login(client)

    student_id, course_id = create_student_and_course(app)

    response = client.post(
        "/api/enrollment/",
        json={
            "student_id": student_id,
            "course_id": course_id,
        },
    )

    assert response.status_code == 201
    assert response.json["message"] == "Enrolled successfully"


def test_enroll_missing_student_or_course(client, app):
    login(client)

    response = client.post(
        "/api/enrollment/",
        json={
            "student_id": 9999,
            "course_id": 9999,
        },
    )

    assert response.status_code == 404
    assert response.json["error"] == ("Student or course not found")


def test_duplicate_enrollment(client, app):
    login(client)

    student_id, course_id = create_student_and_course(app)

    client.post(
        "/api/enrollment/",
        json={
            "student_id": student_id,
            "course_id": course_id,
        },
    )

    response = client.post(
        "/api/enrollment/",
        json={
            "student_id": student_id,
            "course_id": course_id,
        },
    )

    assert response.status_code == 409
    assert response.json["error"] == "Already enrolled"


def test_get_student_courses(client, app):
    student_id, course_id = create_student_and_course(app)

    response = client.get(f"/api/enrollment/student/{student_id}")

    assert response.status_code == 200
    assert response.json == []


def test_remove_enrollment(client, app):
    login(client)

    student_id, course_id = create_student_and_course(app)

    client.post(
        "/api/enrollment/",
        json={
            "student_id": student_id,
            "course_id": course_id,
        },
    )

    response = client.delete(
        f"/api/enrollment/student/" f"{student_id}/course/{course_id}"
    )

    assert response.status_code == 200
    assert response.json["message"] == ("Enrollment removed")


def test_remove_missing_enrollment(client, app):
    login(client)

    student_id, course_id = create_student_and_course(app)

    response = client.delete(
        f"/api/enrollment/student/" f"{student_id}/course/{course_id}"
    )

    assert response.status_code == 404
    assert response.json["error"] == ("Enrollment not found")
