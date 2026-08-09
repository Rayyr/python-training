from ..extensions import db

student_courses = db.Table(
    "student_courses",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True),
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=True)

    user = db.relationship("User", back_populates="student")
    courses = db.relationship(
        "Course",
        secondary=student_courses,
        back_populates="students",
    )
