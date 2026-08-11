from ..extensions import db
from .enrollment import enrollment


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(100),
        nullable=False
    )

    students = db.relationship(
        "Student",
        secondary=enrollment,
        back_populates="courses"
    )
