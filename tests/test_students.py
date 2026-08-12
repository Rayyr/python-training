from app import db
from app.models.student import Student
from app.models.user import User
import os
from io import BytesIO
from tests.conftest import login


def test_students_list_requires_admin(client):

    response = client.get(
        "/students"
    )

    assert response.status_code == 302


def test_admin_can_view_students(client, admin):

    
    client.post("/login",data={"email":  "admin@gmail.com","password": "admin123"})


    response = client.get(
        "/students"
    )

    assert response.status_code == 200


def test_student_cannot_view_student_list(client, student):

    client.post("/login",data={"email":  "john@gmail.com","password": "student123"})


    response = client.get(
        "/students"
    )

    assert response.status_code in (
        302,
        403,
    )


def test_student_profile(client, student):

    
    client.post("/login",data={"email":  "john@gmail.com","password": "student123"})


    response = client.get(
        "/profile"
    )

    assert response.status_code == 200
    assert b"John Student" in response.data


def test_student_can_edit_profile(app, client, student):

    client.post("/login",data={"email":  "john@gmail.com","password": "student123"})


    response = client.post(
        "/profile/edit",
        data={
            "name": "John Updated",
            "email": "john@gmail.com",
            "phone": "0599111111",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        student_obj = Student.query.filter_by(
            email="john@gmail.com"
        ).first()

        assert student_obj.name == "John Updated"
        assert student_obj.phone == "0599111111"


def test_admin_can_access_student_api(client, admin):

   
    client.post("/login",data={"email":  "admin@gmail.com","password": "admin123"})


    response = client.get(
        "/api/students"
    )

    assert response.status_code == 200
    assert response.is_json


def test_student_cannot_access_student_api(client, student):

    client.post("/login",data={"email":  "john@gmail.com","password": "student123"})


    response = client.get(
        "/api/students"
    )

    assert response.status_code in (
        302,
        403,
    )


def test_admin_can_open_create_student(
    client,
    admin,
):

    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.get("/students/new")

    assert response.status_code == 200
 



def test_admin_can_create_student(
    app,
    client,
    admin,
):

    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        "/students/new",
        data={
            "name": "New Student",
            "email": "newstudent@gmail.com",
            "phone": "0599123456",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        student_obj = Student.query.filter_by(
            email="newstudent@gmail.com"
        ).first()

        assert student_obj is not None
        assert student_obj.name == "New Student"
        assert student_obj.phone == "0599123456"

        user = User.query.filter_by(
            email="newstudent@gmail.com"
        ).first()

        assert user is not None
        assert user.role == "student"
        assert user.student_id == student_obj.id

        assert user.check_password("student123")



def test_create_student_duplicate_student_email(
    app,
    client,
    admin,
):

    with app.app_context():

        existing = Student(
            name="Existing Student",
            email="duplicate@gmail.com",
            phone="0599000000",
        )

        db.session.add(existing)
        db.session.commit()

    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        "/students/new",
        data={
            "name": "Another Student",
            "email": "duplicate@gmail.com",
            "phone": "0599111111",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"already exists" in response.data


def test_create_student_duplicate_user_email(
    app,
    client,
    admin,
):

    with app.app_context():

        user = User(
            name="Existing User",
            email="existinguser@gmail.com",
            role="student",
        )

        user.set_password("student123")

        db.session.add(user)
        db.session.commit()

    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        "/students/new",
        data={
            "name": "Another Student",
            "email": "existinguser@gmail.com",
            "phone": "0599111111",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"user account" in response.data.lower()





def test_admin_can_create_student_with_profile_picture(
    app,
    client,
    admin,
):
    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        "/students/new",
        data={
            "name": "Picture Student",
            "email": "picture@gmail.com",
            "phone": "0599000000",
            "profile_picture": (
                BytesIO(b"fake image content"),
                "profile.jpg",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        student = Student.query.filter_by(
            email="picture@gmail.com"
        ).first()

        assert student is not None
        assert student.profile_picture is not None
        assert student.profile_picture.endswith(
            "_profile.jpg"
        )

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            student.profile_picture,
        )

        assert os.path.exists(file_path)


def test_edit_profile_missing_user_session(client):

    with client.session_transaction() as session:
        session["user_id"] = 99999

    response = client.get(
        "/profile/edit",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/login" in response.location

    with client.session_transaction() as session:
        assert "user_id" not in session


def test_admin_cannot_edit_profile(
    client,
    admin,
):

    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.get(
        "/profile/edit",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Administrators should use the admin tools." in response.data


""" def test_not_student_can_edit_profile(
    app,client,student
):
    client """
def test_student_can_update_profile_picture(
    app,
    client,
    student,
):
    client.post(
        "/login",
        data={
            "email": "john@gmail.com",
            "password": "student123",
        },
    )

    response = client.post(
        "/profile/edit",
        data={
            "name": "John Student",
            "email": "john@gmail.com",
            "phone": "0599000000",
            "profile_picture": (
                BytesIO(b"fake image content"),
                "profile.jpg",
            ),
        },
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        student_obj = Student.query.filter_by(
            email="john@gmail.com"
        ).first()

        assert student_obj is not None
        assert student_obj.profile_picture is not None
        assert student_obj.profile_picture.endswith(
            "_profile.jpg"
        )

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            student_obj.profile_picture,
        )

        assert os.path.exists(file_path)