from app import create_app
from app.extensions import db
from app.models import Student

app = create_app()

with app.app_context():
    db.create_all()

    s1 = Student(id="1", name="test1", email="test1@mail.com")
    s2 = Student(id="2", name="test2", email="test2@mail.com")

    db.session.add_all([s1, s2])
    db.session.commit()

    print("Seed data inserted ✅")