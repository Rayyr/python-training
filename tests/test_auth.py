from app import db
from app.models.user import User
from app.models.student import Student

from tests.conftest import login


def test_login_page(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert b"Login" in response.data


def test_signup_page(client):
    response = client.get("/signup")

    assert response.status_code == 200
    assert b"Sign" in response.data


def test_signup_creates_student_and_user(app, client):

    response = client.post(
        "/signup",
        data={
            "name": "Test Student",
            "email": "test@gmail.com",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        user = User.query.filter_by(
            email="test@gmail.com"
        ).first()

        student = Student.query.filter_by(
            email="test@gmail.com"
        ).first()

        assert user is not None
        assert student is not None
        assert user.role == "student"
        assert user.student_id == student.id


def test_signup_password_mismatch(client):

    response = client.post(
        "/signup",
        data={
            "name": "Test Student",
            "email": "test@gmail.com",
            "password": "password123",
            "confirm_password": "different",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Passwords do not match" in response.data


def test_signup_duplicate_email(app, client):

    with app.app_context():

        user = User(
            name="Existing",
            email="existing@gmail.com",
            role="admin",
        )

        user.set_password("password123")

        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/signup",
        data={
            "name": "Another",
            "email": "existing@gmail.com",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"already exists" in response.data


def test_login_invalid_password(client, admin):
    response=client.post("/login",data={"email": "admin@gmail.com","password":"wrong-password"})
     
    assert response.status_code == 200
    assert b"Invalid" in response.data


def test_admin_login(client, admin):
    response=client.get("/login",data={"email": "admin@gmail.com","password":"admin123"})
  
    assert response.status_code == 200


def test_student_login(client, student):
    response=client.get("/login",data={"email": "john@gmail.com","password":"student123"})
 
    assert response.status_code == 200


def test_logout(client, student):

    login(
        client,
        "john@gmail.com",
        "student123",
    )

    response = client.post(
        "/logout",
        follow_redirects=True,
    )

    assert response.status_code == 200


def test_protected_page_requires_login(client):

    response = client.get(
        "/students"
    )

    assert response.status_code in (
        302,
        401,
    )



