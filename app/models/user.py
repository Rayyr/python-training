from flask_login import UserMixin
from ..extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    profile_picture = db.Column(
        db.String(255),
        nullable=True,
        default=None
    )
