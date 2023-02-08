from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])


class EditTaskForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])
