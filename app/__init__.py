from flask import Flask, redirect, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.forms import AddTaskForm, EditTaskForm, SearchForm, AddLabelForm

app = Flask(__name__, static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
app.secret_key = Config.SECRET_KEY
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)
from app.models import Task,Label


@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
def index():
    tasks = db.session.execute(db.select(Task)).scalars()
    labels = db.session.execute(db.select(Label)).scalars()
    sort_by = request.args.get("sort_by")
    filter_by = request.args.get("filter_by")
    order = request.args.get("order")
    addForm = AddTaskForm()
    searchForm = SearchForm()
    addLabelForm = AddLabelForm()
    addForm.labels.choices = [(label.id, label.name) for label in labels]
    if searchForm.validate_on_submit():
        to_do = searchForm.to_do.data
        due_date_sort = searchForm.due_date_sort.data
        search_query='%{0}%'.format(searchForm.text.data)

        if to_do and due_date_sort:
            tasks = db.session.execute(db.select(Task).filter(Task.body.like(search_query), Task.is_done == False).order_by("due_date")).scalars()
        elif to_do:
            tasks = db.session.execute(db.select(Task).filter(Task.body.like(search_query)).filter_by(is_done=False).order_by("due_date")).scalars()
        elif due_date_sort:
            tasks = db.session.execute(db.select(Task).filter(Task.body.like(search_query)).order_by("due_date")).scalars()
        else:
            tasks = db.session.execute(db.select(Task).filter(Task.body.like(search_query))).scalars()

    if addLabelForm.validate_on_submit():
        label = Label(name=addLabelForm.name.data)
        db.session.add(label)
        db.session.commit()

    if addForm.validate_on_submit():
        label_ids = addForm.labels.data
        labels = db.session.query(Label).filter(Label.id.in_(label_ids)).all()
        task = Task(body=addForm.body.data, is_done=False, due_date=addForm.due_date.data, labels=labels)
        db.session.add(task)
        db.session.commit()

    if sort_by:
        if order=="desc":
            tasks =db.session.execute(db.select(Task).order_by(getattr(Task, sort_by).desc())).scalars()
        else:
            tasks =db.session.execute(db.select(Task).order_by(getattr(Task, sort_by))).scalars()
    
    if filter_by:
        tasks =db.session.execute(db.select(Task).filter_by(is_done=bool(filter_by=="True"))).scalars()

    return render_template("index.html", form=addForm, tasks=tasks, searchForm=searchForm, addLabelForm=addLabelForm)

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