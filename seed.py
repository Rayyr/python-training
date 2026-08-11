import click
from app import create_app, db
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User

app = create_app()


@app.cli.command("seed")
def seed():
    """Seed the database with sample students, courses, and enrollments."""
    if Student.query.count() or Course.query.count() or User.query.count():
        click.echo("Database already contains data. Nothing seeded.")
        return

    demo = User(name="Demo Admin", email="admin@example.com")
    demo.set_password("admin123")
    db.session.add(demo)
    db.session.commit()

    students = [
        Student(name="Alice Johnson", email="alice@example.com", phone="+1 555 0101"),
        Student(name="Omar Hassan", email="omar@example.com", phone="+970 599 000 001"),
        Student(name="Sara Williams", email="sara@example.com", phone="+1 555 0103"),
        Student(name="Daniel Lee", email="daniel@example.com", phone="+1 555 0104"),
    ]
    courses = [
        Course(
            code="CS101",
            name="Introduction to Programming",
            description="Programming fundamentals.",
        ),
        Course(
            code="WEB201",
            name="Web Development",
            description="Flask, templates, APIs and frontend development.",
        ),
        Course(code="DB301", name="Database Systems", description="Relational databases and SQL."),
    ]
    db.session.add_all(students + courses)
    db.session.commit()

    db.session.add_all(
        [
            Enrollment(student_id=students[0].id, course_id=courses[0].id),
            Enrollment(student_id=students[0].id, course_id=courses[1].id),
            Enrollment(student_id=students[1].id, course_id=courses[1].id),
            Enrollment(student_id=students[2].id, course_id=courses[2].id),
        ]
    )
    db.session.commit()
    click.echo("Seed data created successfully.")
    click.echo("Demo login: admin@example.com / admin123")


if __name__ == "__main__":
    app.cli.main()
