from app.models.user import User


def test_register_page(client):
    response = client.get("/register")

    assert response.status_code == 200
    assert b"Register" in response.data


def test_register_user(client, app):
    response = client.post(
        "/register",
        data={
            "username": "raya",
            "password": "password123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Registration successful" in response.data

    with app.app_context():
        user = User.query.filter_by(username="raya").first()

        assert user is not None
        assert user.password != "password123"


def test_register_requires_username_and_password(client):
    response = client.post(
        "/register",
        data={},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"required" in response.data


def test_register_duplicate_username(client):
    client.post(
        "/register",
        data={
            "username": "raya",
            "password": "password123",
        },
    )

    response = client.post(
        "/register",
        data={
            "username": "raya",
            "password": "anotherpassword",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"already exists" in response.data


def test_login_success(client):
    client.post(
        "/register",
        data={
            "username": "raya",
            "password": "password123",
        },
    )

    response = client.post(
        "/login",
        data={
            "username": "raya",
            "password": "password123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Login successful" in response.data


def test_login_invalid_password(client):
    client.post(
        "/register",
        data={
            "username": "raya",
            "password": "password123",
        },
    )

    response = client.post(
        "/login",
        data={
            "username": "raya",
            "password": "wrong-password",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_profile_requires_login(client):
    response = client.get("/profile")

    assert response.status_code == 302
    assert "/login" in response.location


def test_logout(client):
    client.post(
        "/register",
        data={
            "username": "raya",
            "password": "password123",
        },
    )

    client.post(
        "/login",
        data={
            "username": "raya",
            "password": "password123",
        },
    )

    response = client.get(
        "/logout",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You have been logged out" in response.data
