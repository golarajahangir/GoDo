import os
os.environ['DATABASE_URL'] = 'sqlite://'  # use an in-memory database for tests

import unittest
from datetime import datetime
from app import app, db
from app.models import Task

class TaskModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_task_creation(self):
        task = Task(body='testtask', due_date=datetime.utcnow(), is_done=False, created_at=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        self.assertEqual(Task.query.filter_by(body='testtask').first(), task)


if __name__ == '__main__':
    unittest.main()