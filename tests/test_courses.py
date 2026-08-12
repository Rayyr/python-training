from app import db
from app.models.course import Course
from app.models.user import User
from app.models.enrollment import Enrollment
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


def test_create_course_uppercases_code(
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
        "/courses/new",
        data={
            "code": "web201",
            "name": "Web Development",
            "description": "Flask development",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        course = Course.query.filter_by(
            code="WEB201"
        ).first()

        assert course is not None
        assert course.code == "WEB201"



def test_admin_cannot_create_duplicate_course(
    app,
    client,
    admin,
    course,
):
    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        "/courses/new",
        data={
            "code": "CS101",
            "name": "Another Programming Course",
            "description": "Duplicate course",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert (
        b"A course with that code already exists."
        in response.data
    )

    with app.app_context():

        courses = Course.query.filter_by(
            code="CS101"
        ).all()

        assert len(courses) == 1




def test_admin_can_open_edit_course(
    client,
    admin,
    course,
):
    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.get(
        f"/courses/{course}/edit"
    )

    assert response.status_code == 200



def test_edit_course_uppercases_code(
    app,
    client,
    admin,
    course,
):
    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        f"/courses/{course}/edit",
        data={
            "code": "web202",
            "name": "Web Programming",
            "description": "Web programming",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():

        updated_course = db.session.get(
            Course,
            course,
        )

        assert updated_course.code == "WEB202"



def test_admin_cannot_edit_course_to_duplicate_code(
    app,
    client,
    admin,
    course,
):
    with app.app_context():

        other_course = Course(
            code="WEB201",
            name="Web Development",
            description="Another course",
        )

        db.session.add(other_course)
        db.session.commit()

    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        f"/courses/{course}/edit",
        data={
            "code": "web201",
            "name": "Changed Name",
            "description": "Changed description",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert (
        b"That course code is already in use."
        in response.data
    )



def test_api_get_course_enrollments(
    app,
    client,
    admin,
    student,
    course,
):
    with app.app_context():

        user = db.session.get(
            User,
            student,
        )

        enrollment = Enrollment(
            student_id=user.student.id,
            course_id=course,
        )

        db.session.add(enrollment)
        db.session.commit()

    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.get(
        f"/api/courses/{course}/enrollments"
    )

    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["name"] == "John Student"
    assert data[0]["email"] == "john@gmail.com"



def test_api_get_course_enrollments_empty(
    client,
    admin,
    course,
):
    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.get(
        f"/api/courses/{course}/enrollments"
    )

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == []


def test_api_enrollments_course_not_found(
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
        "/api/courses/999999/enrollments"
    )

    assert response.status_code == 404



def test_api_enrollments_requires_login(
    client,
    course,
):
    response = client.get(
        f"/api/courses/{course}/enrollments"
    )

    assert response.status_code in (
        302,
        401,
    )


def test_api_enroll_missing_student_id(
    client,
    admin,
    course,
):
    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        f"/api/courses/{course}/enrollments",
        json={},
    )

    assert response.status_code == 400
    assert response.is_json

    data = response.get_json()

    assert data["error"] == "student_id is required"



def test_api_enroll_without_json(
    client,
    admin,
    course,
):
    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        f"/api/courses/{course}/enrollments",
    )

    assert response.status_code == 400
    assert response.is_json

    assert (
        response.get_json()["error"]
        == "student_id is required"
    )



def test_api_enroll_already_enrolled(
    app,
    client,
    admin,
    student,
    course,
):
    with app.app_context():

        user = db.session.get(
            User,
            student,
        )

        enrollment = Enrollment(
            student_id=user.student.id,
            course_id=course,
        )

        db.session.add(enrollment)
        db.session.commit()

        student_id = user.student.id

    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        f"/api/courses/{course}/enrollments",
        json={
            "student_id": student_id,
        },
    )

    assert response.status_code == 409
    assert response.is_json

    data = response.get_json()

    assert data["error"] == "Already enrolled"



def test_api_enroll_student(
    app,
    client,
    admin,
    student,
    course,
):
    with app.app_context():

        user = db.session.get(
            User,
            student,
        )

        student_id = user.student.id

    client.post(
        "/login",
        data={
            "email": "admin@gmail.com",
            "password": "admin123",
        },
    )

    response = client.post(
        f"/api/courses/{course}/enrollments",
        json={
            "student_id": student_id,
        },
    )

    assert response.status_code == 201
    assert response.is_json

    data = response.get_json()

    assert data["message"] == "Enrollment created"
    assert data["id"] is not None

    with app.app_context():

        enrollment = Enrollment.query.filter_by(
            student_id=student_id,
            course_id=course,
        ).first()

        assert enrollment is not None
        assert enrollment.id == data["id"]