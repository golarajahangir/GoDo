from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Optional


class AddTaskForm(FlaskForm):
    body = StringField("What are you going to do?", validators=[DataRequired()])
    due_date = DateField("Due date", validators=[Optional()])
    labels = SelectMultipleField("Choose labels", validate_choice=False, coerce=int)


class EditTaskForm(FlaskForm):
    body = StringField("", validators=[DataRequired()])
    is_done = BooleanField("Have you finished your task?")
    due_date = DateField("Due date", validators=[Optional()])

class SearchForm(FlaskForm):
    text = StringField("")
    to_do = BooleanField("Not Done")
    due_date_sort = BooleanField("Search and sort asc on due date")

class AddLabelForm(FlaskForm):
    name= StringField("Add new label", validators=[DataRequired()])