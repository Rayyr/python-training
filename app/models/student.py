from app import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(30))
    profile_picture = db.Column(db.String(255))

    enrollments = db.relationship(
        "Enrollment", back_populates="student", cascade="all, delete-orphan"
    )

    courses = db.relationship(
        "Course", secondary="enrollments", back_populates="students", viewonly=True
    )

    def __repr__(self):
        return f"<Student {self.name}>"
