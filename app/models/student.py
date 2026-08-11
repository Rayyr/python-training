from ..extensions import db
from .enrollment import enrollment

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    courses=db.relationship("Course",secondary=enrollment,back_populates="students")
