from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from app.forms import AddTaskForm, EditTaskForm
from app.config import Config

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
app.secret_key = Config.SECRET_KEY
db.init_app(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from app.models import Task


@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
def index():
    tasks = db.session.execute(db.select(Task)).scalars()
    addForm = AddTaskForm()
    if addForm.validate_on_submit():
        task = Task(body=addForm.body.data, status=False)
        db.session.add(task)
        db.session.commit()
    return render_template("index.html", form=addForm, tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task = db.get_or_404(Task, id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    editForm = EditTaskForm()
    task = db.get_or_404(Task, id)
    if editForm.validate_on_submit():
        task.body = editForm.body.data
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", form=editForm, task=task)
