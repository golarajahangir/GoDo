from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    is_done = db.Column(db.Boolean)
    due_date = db.Column(db.DateTime)
