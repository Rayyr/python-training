from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="student",
    )

    # Links a login account to its Student record.
    # Admin accounts can have NULL here.
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        unique=True,
        nullable=True,
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "user",
            uselist=False,
        ),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password,
        )

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_student(self):
        return self.role == "student"

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
