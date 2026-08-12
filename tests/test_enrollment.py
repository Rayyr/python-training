from app import db
from app.models.enrollment import Enrollment

from tests.conftest import login


def test_student_can_enroll(
    app,
    client,
    student,
    course,
):

   
    client.post("/login",data={"email":  "john@gmail.com","password": "student123"})


    response = client.post(
        f"/courses/{course}/enroll",
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        enrollment = Enrollment.query.filter_by(
            course_id=course,
        ).first()

        assert enrollment is not None


def test_student_cannot_enroll_twice(
    app,
    client,
    student,
    course,
):

    client.post("/login",data={"email":  "john@gmail.com","password": "student123"})

    client.post(
        f"/courses/{course}/enroll"
    )

    response = client.post(
        f"/courses/{course}/enroll",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"already enrolled" in response.data

    with app.app_context():

        enrollments = Enrollment.query.filter_by(
            course_id=course,
        ).all()

        assert len(enrollments) == 1


def test_student_can_unenroll(
    app,
    client,
    student,
    course,
):

    login(
        client,
        "john@gmail.com",
        "student123",
    )

    client.post(
        f"/courses/{course}/enroll"
    )

    response = client.post(
        f"/courses/{course}/unenroll",
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        enrollment = Enrollment.query.filter_by(
            course_id=course,
        ).first()

        assert enrollment is None


def test_enroll_requires_login(
    client,
    course,
):

    response = client.post(
        f"/courses/{course}/enroll"
    )

    assert response.status_code == 302
