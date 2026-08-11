from app.extensions import db
from app.models.student import Student


def test_students_page(client):
    response = client.get("/students/")

    assert response.status_code == 200


def test_add_student(client, app):
    response = client.post(
        "/students/add",
        data={
            "name": "Raya",
            "email": "raya@example.com",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Student added successfully" in response.data

    with app.app_context():
        student = Student.query.filter_by(email="raya@example.com").first()

        assert student is not None
        assert student.name == "Raya"


def test_add_student_requires_fields(client):
    response = client.post(
        "/students/add",
        data={},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Name and email are required" in response.data


def test_duplicate_student_email(client):
    client.post(
        "/students/add",
        data={
            "name": "Raya",
            "email": "raya@example.com",
        },
    )

    response = client.post(
        "/students/add",
        data={
            "name": "Another Raya",
            "email": "raya@example.com",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"already exists" in response.data


def test_search_students(client, app):
    with app.app_context():
        db.session.add(
            Student(
                name="Alice",
                email="alice@example.com",
            )
        )
        db.session.add(
            Student(
                name="Bob",
                email="bob@example.com",
            )
        )
        db.session.commit()

    response = client.get("/students/?search=Alice")

    assert response.status_code == 200
    assert b"Alice" in response.data
