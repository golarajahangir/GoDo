from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField
from wtforms.validators import DataRequired, Optional


class AddTaskForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])
    due_date = DateField("Due date", validators=[Optional()])


class EditTaskForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])
    is_done = BooleanField("Have you finished your task?")
    due_date = DateField("Due date", validators=[Optional()])

class SearchForm(FlaskForm):
    text = StringField("")
