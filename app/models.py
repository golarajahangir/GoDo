from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean)
