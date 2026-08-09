from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.student import Student
from app.models.course import Course

app = create_app()

with app.app_context():
    db.create_all()

    accounts = [
        ("admin", "admin123", "admin"),
        ("instructor", "instructor123", "instructor"),
        ("student", "student123", "student"),
    ]

    users = {}
    for username, password, role in accounts:
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
        users[username] = user

    student = Student.query.filter_by(email="student@example.com").first()
    if not student:
        student = Student(
            name="Demo Student",
            email="student@example.com",
            user_id=users["student"].id,
        )
        db.session.add(student)

    if Course.query.count() == 0:
        db.session.add_all([
            Course(title="Python Fundamentals", description="Core Python programming"),
            Course(title="Flask Web Development", description="Build Flask applications"),
            Course(title="Database Design", description="Relational database fundamentals"),
        ])

    db.session.commit()
    print("Seed complete.")
    print("admin / admin123")
    print("instructor / instructor123")
    print("student / student123")
