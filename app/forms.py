from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=100)]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")


class ProfilePictureForm(FlaskForm):
    picture = FileField(
        "Profile Picture",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "jpeg", "png", "gif"],
                "Images only!"
            )
        ]
    )

    submit = SubmitField("Upload")
