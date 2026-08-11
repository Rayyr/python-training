from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CourseForm(FlaskForm):
    code = StringField("Course Code", validators=[DataRequired(), Length(min=2, max=30)])
    name = StringField("Course Name", validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField("Description")
    submit = SubmitField("Save Course")
