from app import db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.user import User


def test_model_repr_and_relationships(app):
    with app.app_context():
        student = Student(name="Alice", email="alice@example.com")
        course = Course(code="CS101", name="Programming")
        user = User(name="Alice", email="user@example.com")
        user.set_password("secret123")
        db.session.add_all([student, course, user])
        db.session.commit()

        enrollment = Enrollment(student_id=student.id, course_id=course.id)
        db.session.add(enrollment)
        db.session.commit()

        assert repr(student) == "<Student Alice>"
        assert repr(course) == "<Course CS101>"
        assert student.enrollments[0].course is course
        assert course.enrollments[0].student is student
        assert student.courses[0] is course
        assert course.students[0] is student
        assert user.check_password("secret123")
        assert not user.check_password("bad")
