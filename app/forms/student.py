from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class StudentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField("Phone", validators=[Length(max=30)])
    profile_picture = FileField(
        "Profile Picture", validators=[FileAllowed(["jpg", "jpeg", "png", "gif"], "Images only.")]
    )
    submit = SubmitField("Save Student")
