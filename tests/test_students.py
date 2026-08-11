from io import BytesIO

from app import db
from app.models.course import Course
from app.models.student import Student


def login(client, email="student-tests@example.com"):
    return client.post(
        "/signup",
        data={
            "name": "Test User",
            "email": email,
            "password": "secret123",
            "confirm_password": "secret123",
        },
    )


def add_student(app, name="Student", email="student@example.com", phone="123"):
    with app.app_context():
        student = Student(name=name, email=email, phone=phone)
        db.session.add(student)
        db.session.commit()
        return student.id


def add_course(app, code="CS101", name="Programming"):
    with app.app_context():
        course = Course(code=code, name=name, description="Description")
        db.session.add(course)
        db.session.commit()
        return course.id


def test_students_page_and_search(client, app):
    login(client)
    add_student(app, "Alice Johnson", "alice@example.com")
    add_student(app, "Bob Smith", "bob@example.com")

    response = client.get("/students")
    assert response.status_code == 200
    assert b"Alice Johnson" in response.data
    assert b"Bob Smith" in response.data

    response = client.get("/students?q=alice")
    assert b"Alice Johnson" in response.data
    assert b"Bob Smith" not in response.data


def test_students_pagination(client, app):
    login(client)
    for i in range(7):
        add_student(app, f"Student {i}", f"student{i}@example.com")

    response = client.get("/students?page=2")
    assert response.status_code == 200
    assert b"Student 6" in response.data


def test_create_student_duplicate_and_invalid(client, app):
    login(client)
    add_student(app, "Existing", "existing@student.com")

    response = client.post(
        "/students/new",
        data={"name": "Existing Again", "email": "existing@student.com", "phone": "123"},
    )
    assert b"already exists" in response.data

    response = client.post("/students/new", data={"name": "", "email": "not-an-email", "phone": ""})
    assert response.status_code == 200
    assert b"Add Student" in response.data


def test_create_student_with_profile_picture(client, app, tmp_path):
    login(client)
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    client.application.config["UPLOAD_FOLDER"] = str(upload_dir)

    response = client.post(
        "/students/new",
        data={
            "name": "Photo Student",
            "email": "photo@example.com",
            "phone": "555",
            "profile_picture": (BytesIO(b"fake image data"), "profile.jpg"),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 302
    with app.app_context():
        student = Student.query.filter_by(email="photo@example.com").first()
        assert student is not None
        assert student.profile_picture.endswith("_profile.jpg")
        assert (upload_dir / student.profile_picture).exists()


def test_edit_student_success_duplicate_and_upload(client, app, tmp_path):
    login(client)
    student_id = add_student(app, "Edit Me", "edit@example.com")
    add_student(app, "Other", "other@example.com")

    response = client.post(
        f"/students/{student_id}/edit",
        data={"name": "Edited Name", "email": "other@example.com", "phone": "999"},
    )
    assert b"already in use" in response.data

    response = client.post(
        f"/students/{student_id}/edit",
        data={"name": "Edited Name", "email": "edited@example.com", "phone": "999"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Edited Name" in response.data

    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    client.application.config["UPLOAD_FOLDER"] = str(upload_dir)
    response = client.post(
        f"/students/{student_id}/edit",
        data={
            "name": "Edited Again",
            "email": "edited@example.com",
            "phone": "111",
            "profile_picture": (BytesIO(b"image"), "avatar.png"),
        },
    )
    assert response.status_code == 302


def test_student_detail_enroll_duplicate_unenroll(client, app):
    login(client)
    student_id = add_student(app, "Enrolled Student", "enrolled@example.com")
    course_id = add_course(app, "WEB101", "Web Development")

    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert b"Enrolled Student" in response.data

    response = client.post(f"/students/{student_id}/enroll", data={"course_id": course_id})
    assert response.status_code == 302

    response = client.post(
        f"/students/{student_id}/enroll",
        data={"course_id": course_id},
        follow_redirects=True,
    )
    assert b"already enrolled" in response.data

    response = client.post(f"/students/{student_id}/unenroll/{course_id}", follow_redirects=True)
    assert response.status_code == 200
    assert b"Enrolled Student" in response.data


def test_student_delete(client, app):
    login(client)
    student_id = add_student(app, "Delete Me", "delete@example.com")
    response = client.post(f"/students/{student_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        assert db.session.get(Student, student_id) is None


def test_students_api_list_and_search(client, app):
    login(client)
    add_student(app, "API Alice", "api-alice@example.com", "111")
    add_student(app, "API Bob", "api-bob@example.com", "222")

    response = client.get("/api/students")
    assert response.status_code == 200
    assert len(response.json) >= 2

    response = client.get("/api/students?q=Alice")
    assert response.status_code == 200
    assert response.json[0]["name"] == "API Alice"


def test_student_api_get_put_delete(client, app):
    login(client)
    student_id = add_student(app, "API Student", "api@example.com", "123")

    response = client.get(f"/api/students/{student_id}")
    assert response.status_code == 200
    assert response.json["email"] == "api@example.com"

    response = client.put(
        f"/api/students/{student_id}",
        json={"name": "Updated API", "phone": "999"},
    )
    assert response.status_code == 200
    assert response.json["message"] == "Student updated"

    response = client.put(f"/api/students/{student_id}", json={})
    assert response.status_code == 200

    response = client.delete(f"/api/students/{student_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Student deleted"


def test_student_api_not_found(client):
    login(client)
    response = client.get("/api/students/99999")
    assert response.status_code == 404
