from ..extensions import db

enrollment = db.Table(
    "enrollment",
    db.Column(
        "student_id",
        db.Integer,
        db.ForeignKey("student.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "course_id",
        db.Integer,
        db.ForeignKey("course.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
