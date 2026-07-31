import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_add_student(client):
    response = client.post("/register", data={
        "name": "Test",
        "id": "1",
        "email": "test@mail.com"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Test" in response.data


def test_students_page(client):
    response = client.get("/students")
    assert response.status_code == 200


def test_student_detail(client):
    client.post("/register", data={
        "name": "Detail",
        "id": "99",
        "email": "d@mail.com"
    })

    response = client.get("/student/99")
    assert response.status_code == 200
    assert b"Detail" in response.data