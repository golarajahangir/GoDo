from app import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    labels = db.relationship("Label", secondary="task_label", backref="tasks")


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

task_label = db.Table("task_label", 
       db.Column("task_id", db.Integer, db.ForeignKey("task.id"), primary_key = True),             
       db.Column("label_id", db.Integer, db.ForeignKey("label.id"), primary_key = True)               
                      ) 