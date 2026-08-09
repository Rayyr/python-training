from ..extensions import db
from .student import student_courses

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    students = db.relationship(
        "Student",
        secondary=student_courses,
        back_populates="courses",
    )
