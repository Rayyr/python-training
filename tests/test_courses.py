from app.extensions import db
from app.models.course import Course


def test_courses_page(client):
    response = client.get("/courses/")

    assert response.status_code == 200


def test_add_course(client, app):
    response = client.post(
        "/courses/add",
        data={
            "title": "Python Testing",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Course added successfully" in response.data

    with app.app_context():
        course = Course.query.filter_by(title="Python Testing").first()

        assert course is not None


def test_add_course_requires_title(client):
    response = client.post(
        "/courses/add",
        data={},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Course title is required" in response.data


def test_search_courses(client, app):
    with app.app_context():
        db.session.add(Course(title="Python"))
        db.session.add(Course(title="Java"))
        db.session.commit()

    response = client.get("/courses/?search=Python")

    assert response.status_code == 200
    assert b"Python" in response.data
