from app import db
from app.models.student import Student
from app.models.user import User


def test_signup_page(client):
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"Create an account" in response.data


def test_signup_validation_branches(client):
    # Missing required fields
    response = client.post("/signup", data={"name": "", "email": "", "password": ""})
    assert b"All fields are required" in response.data

    # Password too short
    response = client.post(
        "/signup",
        data={
            "name": "Short",
            "email": "short@example.com",
            "password": "12345",
            "confirm_password": "12345",
        },
    )
    assert b"at least 6 characters" in response.data

    # Password mismatch
    response = client.post(
        "/signup",
        data={
            "name": "Mismatch",
            "email": "mismatch@example.com",
            "password": "123456",
            "confirm_password": "654321",
        },
    )
    assert b"Passwords do not match" in response.data


def test_signup_creates_user_and_student(client, app):
    response = client.post(
        "/signup",
        data={
            "name": "New Student",
            "email": "newstudent@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"New Student" in response.data

    with app.app_context():
        user = User.query.filter_by(email="newstudent@example.com").first()
        student = Student.query.filter_by(email="newstudent@example.com").first()
        assert user is not None
        assert student is not None
        assert student.name == "New Student"
        assert user.check_password("secret123")
        assert not user.check_password("wrong-password")


def test_signup_duplicate_email(client, app):
    with app.app_context():
        user = User(name="Existing", email="existing@example.com")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/signup",
        data={
            "name": "Another",
            "email": " EXISTING@example.com ",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    )
    assert b"already exists" in response.data


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_invalid_user_and_wrong_password(client, app):
    response = client.post("/login", data={"email": "missing@example.com", "password": "secret123"})
    assert b"Invalid email or password" in response.data

    with app.app_context():
        user = User(name="Login User", email="login@example.com")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

    response = client.post("/login", data={"email": "login@example.com", "password": "wrong"})
    assert b"Invalid email or password" in response.data


def test_login_success_safe_next(client, app):
    with app.app_context():
        user = User(name="Login User", email="login@example.com")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login?next=/courses", data={"email": "LOGIN@example.com", "password": "secret123"}
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/courses")


def test_login_success_unsafe_next_falls_back(client, app):
    with app.app_context():
        user = User(name="Safe User", email="safe@example.com")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login?next=https://evil.example.com",
        data={"email": "safe@example.com", "password": "secret123"},
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/students")


def test_logout(client):
    client.post(
        "/signup",
        data={
            "name": "Logout User",
            "email": "logout@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    )
    response = client.post("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_required_redirect(client):
    response = client.get("/students")
    assert response.status_code == 302
    assert "/login?next=/students" in response.headers["Location"]


def test_root_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/students" in response.headers["Location"]


def test_current_user_is_available_in_templates(client):
    client.post(
        "/signup",
        data={
            "name": "Context User",
            "email": "context@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    )
    response = client.get("/students")
    assert b"Hi, Context User" in response.data
