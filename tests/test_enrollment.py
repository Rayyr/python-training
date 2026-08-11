from app.extensions import db
from app.models.student import Student
from app.models.course import Course

def test_student_multiple_courses(app):
    with app.app_context():
        s=Student(name="John",email="john@test.com")
        c1=Course(title="Python")
        c2=Course(title="Flask")
        s.courses.extend([c1,c2])
        db.session.add(s)
        db.session.commit()
        assert len(s.courses)==2
        assert c1 in s.courses
        assert c2 in s.courses

def test_course_multiple_students(app):
    with app.app_context():
        s1=Student(name="John",email="john@test.com")
        s2=Student(name="Jane",email="jane@test.com")
        c=Course(title="Python")
        s1.courses.append(c)
        s2.courses.append(c)
        db.session.add_all([s1,s2])
        db.session.commit()
        assert len(c.students)==2
