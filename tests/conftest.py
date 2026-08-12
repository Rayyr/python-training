import os

import pytest
from dotenv import load_dotenv

from app import create_app, db
from app.models.user import User
from app.models.student import Student
from app.models.course import Course


# Load variables from .env
load_dotenv()


@pytest.fixture
def app(tmp_path):

    app = create_app(
        {
            "TESTING": True,

            # Use a separate test database.
            # Do NOT use your development student_portal.db
            # for automated tests.
            "SQLALCHEMY_DATABASE_URI": os.getenv(
                "TEST_DATABASE_URL",
                "sqlite:///:memory:",
            ),

            "WTF_CSRF_ENABLED": False,

            "UPLOAD_FOLDER": os.getenv(
                "TEST_UPLOAD_FOLDER",
                str(tmp_path),
            ),

            "SECRET_KEY": os.getenv(
                "SECRET_KEY",
                "dev-secret-change-me",
            ),
        }
    )

    with app.app_context():

        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin(app):

    with app.app_context():

        user = User(
            name=os.getenv(
                "TEST_ADMIN_NAME",
                "Admin",
            ),
            email=os.getenv(
                "TEST_ADMIN_EMAIL",
                "admin@gmail.com",
            ),
            role="admin",
        )

        user.set_password(
            os.getenv(
                "TEST_ADMIN_PASSWORD",
                "admin123",
            )
        )

        db.session.add(user)
        db.session.commit()

        return user.id


@pytest.fixture
def student(app):

    with app.app_context():

        student = Student(
            name=os.getenv(
                "TEST_STUDENT_NAME",
                "John Student",
            ),
            email=os.getenv(
                "TEST_STUDENT_EMAIL",
                "john@gmail.com",
            ),
            phone=os.getenv(
                "TEST_STUDENT_PHONE",
                "0599000000",
            ),
        )

        db.session.add(student)
        db.session.flush()

        user = User(
            name=student.name,
            email=student.email,
            role="student",
            student_id=student.id,
        )

        user.set_password(
            os.getenv(
                "TEST_STUDENT_PASSWORD",
                "student123",
            )
        )

        db.session.add(user)
        db.session.commit()

        return user.id


@pytest.fixture
def course(app):

    with app.app_context():

        course = Course(
            code=os.getenv(
                "TEST_COURSE_CODE",
                "CS101",
            ),
            name=os.getenv(
                "TEST_COURSE_NAME",
                "Programming",
            ),
            description=os.getenv(
                "TEST_COURSE_DESCRIPTION",
                "Python programming",
            ),
        )

        db.session.add(course)
        db.session.commit()

        return course.id


def login(client, email, password):

    return client.post(
        "/auth/login",
        data={
            "email": email,
            "password": password,
        },
        follow_redirects=True,
    )


