from flask import Flask, redirect, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.forms import AddTaskForm, EditTaskForm, SearchForm

app = Flask(__name__, static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
app.secret_key = Config.SECRET_KEY
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)
from app.models import Task


@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
def index():
    tasks = db.session.execute(db.select(Task)).scalars()
    sort_by = request.args.get("sort_by")
    order = request.args.get("order")
    addForm = AddTaskForm()
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        search_query='%{0}%'.format(searchForm.text.data)
        tasks = db.session.query(Task).filter(Task.body.like(search_query))
    if addForm.validate_on_submit():
        task = Task(body=addForm.body.data, is_done=False, due_date=addForm.due_date.data)
        db.session.add(task)
        db.session.commit()
        return render_template("index.html", form=addForm, tasks=tasks, searchForm=searchForm)

    if sort_by=="created_at" and order=="asc":
        tasks =db.session.execute(db.select(Task).order_by(Task.created_at)).scalars()
    elif sort_by=="created_at" and order=="desc":
        tasks =db.session.execute(db.select(Task).order_by(Task.created_at.desc())).scalars()

    if sort_by=="due_date" and order=="asc":
        tasks =db.session.execute(db.select(Task).order_by(Task.due_date)).scalars()
    elif sort_by=="due_date" and order=="desc":
        tasks =db.session.execute(db.select(Task).order_by(Task.due_date.desc())).scalars()
            
    if sort_by=="is_done":
        tasks =db.session.execute(db.select(Task).filter_by(is_done=True)).scalars()
    if sort_by=="not_done":
        tasks =db.session.execute(db.select(Task).filter_by(is_done=False)).scalars()

    return render_template("index.html", form=addForm, tasks=tasks, searchForm=searchForm)

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
        task.is_done = editForm.is_done.data
        task.due_date = editForm.due_date.data
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", form=editForm, task=task)


