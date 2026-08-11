from app import db


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)

    enrollments = db.relationship(
        "Enrollment", back_populates="course", cascade="all, delete-orphan"
    )

    students = db.relationship(
        "Student", secondary="enrollments", back_populates="courses", viewonly=True
    )

    def __repr__(self):
        return f"<Course {self.code}>"
