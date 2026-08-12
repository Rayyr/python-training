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

    # ---------------------------------------------------------
    # Create admin user
    # ---------------------------------------------------------
    admin = User.query.filter_by(email="admin@example.com").first()

    if not admin:
        admin = User(
            name="System Administrator",
            email="admin@example.com",
            role="admin",
        )

        admin.set_password("admin123")

        db.session.add(admin)

        click.echo("Admin user created.")
    else:
        click.echo("Admin user already exists.")

    db.session.commit()

    # ---------------------------------------------------------
    # Create demo students
    # ---------------------------------------------------------
    if Student.query.count() == 0:

        students = [
            Student(
                name="Alice Johnson",
                email="alice@example.com",
                phone="+1 555 0101",
            ),
            Student(
                name="Omar Hassan",
                email="omar@example.com",
                phone="+970 599 000 001",
            ),
            Student(
                name="Sara Williams",
                email="sara@example.com",
                phone="+1 555 0103",
            ),
            Student(
                name="Daniel Lee",
                email="daniel@example.com",
                phone="+1 555 0104",
            ),
        ]

        db.session.add_all(students)
        db.session.commit()

        click.echo("Demo students created.")

    else:
        click.echo("Students already exist.")

    # ---------------------------------------------------------
    # Create demo courses
    # ---------------------------------------------------------
    if Course.query.count() == 0:

        courses = [
            Course(
                code="CS101",
                name="Introduction to Programming",
                description="Programming fundamentals.",
            ),
            Course(
                code="WEB201",
                name="Web Development",
                description=("Flask, templates, APIs and frontend development."),
            ),
            Course(
                code="DB301",
                name="Database Systems",
                description="Relational databases and SQL.",
            ),
        ]

        db.session.add_all(courses)
        db.session.commit()

        click.echo("Demo courses created.")

    else:
        click.echo("Courses already exist.")

    # ---------------------------------------------------------
    # Create enrollments
    # ---------------------------------------------------------
    if Enrollment.query.count() == 0:

        alice = Student.query.filter_by(email="alice@example.com").first()

        omar = Student.query.filter_by(email="omar@example.com").first()

        sara = Student.query.filter_by(email="sara@example.com").first()

        cs101 = Course.query.filter_by(code="CS101").first()

        web201 = Course.query.filter_by(code="WEB201").first()

        db301 = Course.query.filter_by(code="DB301").first()

        enrollments = [
            Enrollment(
                student_id=alice.id,
                course_id=cs101.id,
            ),
            Enrollment(
                student_id=alice.id,
                course_id=web201.id,
            ),
            Enrollment(
                student_id=omar.id,
                course_id=web201.id,
            ),
            Enrollment(
                student_id=sara.id,
                course_id=db301.id,
            ),
        ]

        db.session.add_all(enrollments)
        db.session.commit()

        click.echo("Demo enrollments created.")

    else:
        click.echo("Enrollments already exist.")

    # ---------------------------------------------------------
    # Finished
    # ---------------------------------------------------------
    click.echo("")
    click.echo("====================================")
    click.echo("Database seeding completed.")
    click.echo("====================================")
    click.echo("Admin login:")
    click.echo("Email: admin@example.com")
    click.echo("Password: admin123")


if __name__ == "__main__":
    app.cli.main()
