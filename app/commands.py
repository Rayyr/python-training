import click
from .extensions import db
from .models.student import Student
from .models.course import Course

def register_commands(app):
    @app.cli.command("seed")
    def seed():
        if Student.query.first() or Course.query.first():
            click.echo("Database already contains data.")
            return
        s1=Student(name="John Doe",email="john@example.com")
        s2=Student(name="Jane Smith",email="jane@example.com")
        c1=Course(title="Python")
        c2=Course(title="Flask")
        s1.courses.extend([c1,c2])
        s2.courses.append(c1)
        db.session.add_all([s1,s2,c1,c2])
        db.session.commit()
        click.echo("Database seeded successfully!")
