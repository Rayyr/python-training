from app import db
from app.models.course import Course

from tests.conftest import login


def test_courses_requires_login(client):

    response = client.get(
        "/courses"
    )

    assert response.status_code == 302


def test_student_can_view_courses(
    client,
    student,
):

    client.post("/login",data={"email": "john@gmail.com","password":"student123"})
 

    response = client.get(
        "/courses"
    )

    assert response.status_code == 200


def test_admin_can_view_courses(
    client,
    admin,
):

    client.post("/login",data={"email": "admin@gmail.com","password":"admin123"})


    response = client.get(
        "/courses"
    )

    assert response.status_code == 200


def test_admin_can_open_create_course(
    client,
    admin,
):

    client.post("/login",data={"email": "admin@gmail.com","password":"admin123"})


    response = client.get(
        "/courses/new"
    )

    assert response.status_code == 200


def test_student_cannot_create_course(
    client,
    student,
):

    client.post("/login",data={"email": "john@gmail.com","password":"student123"})


    response = client.get(
        "/courses/new"
    )

    assert response.status_code in (
        302,
        403,
    )


def test_course_filter(
    client,
    admin,
    course,
):
    
    client.post("/login",data={"email": "admin@gmail.com","password":"admin123"})


    response = client.get(
        "/courses?q=CS101"
    )

    assert response.status_code == 200
    assert b"CS101" in response.data


def test_course_pagination(
    client,
    admin,
    app,
):

    client.post("/login",data={"email": "admin@gmail.com","password":"admin123"})

    with app.app_context():

        for i in range(10):

            db.session.add(
                Course(
                    code=f"TEST{i}",
                    name=f"Test Course {i}",
                    description="Testing",
                )
            )

        db.session.commit()

    login(
        client,
        "admin@gmail.com",
        "admin123",
    )

    response = client.get(
        "/courses?page=2"
    )

    assert response.status_code == 200


def test_student_cannot_delete_course(
    client,
    student,
    course,
):

    login(
        client,
        "john@gmail.com",
        "student123",
    )

    response = client.post(
        f"/courses/{course}/delete"
    )

    assert response.status_code in (
        302,
        403,
    )


def test_admin_can_delete_course(
    app,
    client,
    admin,
    course,
):

    client.post("/login",data={"email": "admin@gmail.com","password":"admin123"})


    response = client.post(
        f"/courses/{course}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        assert db.session.get(
            Course,
            course,
        ) is None
