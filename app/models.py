from .extensions import db

class Student(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)