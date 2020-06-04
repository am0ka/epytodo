from app import *
from app.models import *
from app.api import *
from flask import *

class MainCtrl(object):
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.user = User(self.app, self.db)

    def index(self):
        return render_template("index.html", page_title="Home page")

class AuthCtrl(object):
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.api = API(self.app, self.db)

    def registration(self, req):
        _username = req.form['username']
        _password = req.form['password']
        _res = self.api.user_add(_username, _password)
        flash(json.loads(_res))
        return redirect(url_for('index_route'))
    
    def login(self, req):
        _username = req.form['username']
        _password = req.form['password']
        _res = self.api.user_in(_username, _password)
        flash(json.loads(_res))
        return redirect(url_for('index_route'))
    
    def logout(self, req):
        _res = self.api.user_out()
        flash(json.loads(_res))
        return redirect(url_for('index_route'))

class UserCtrl(object):
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.api = API(self.app, self.db)
    
    def info(self):
        _tasks = json.loads(self.api.select_all_tasks(session['id']))
        _undone = _done = _inprog = 0
        for task in _tasks['result']:
            if task[4] == "not started":
                _undone += 1
            elif task[4] == "in progress":
                _inprog += 1
            elif task[4] == "done":
                _done += 1
        return render_template("dashboard.html", page_title="Dashboard", undone=_undone, done=_done, \
            inprog=_inprog, tcount=len(_tasks['result']))

    def all_tasks(self):
        _tasks = json.loads(self.api.select_all_tasks(session['id']))
        return render_template("tasks.html", tlist=_tasks['result'])

    def get_task(self, tid):
        _tasks = json.loads(self.api.get_task(tid))
        if 'error' in _tasks:
            flash(_tasks)
        return render_template("modals/task.html", task=_tasks['result'])

class TaskCtrl(object):
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.api = API(self.app, self.db)
    
    def create(self, req):
        _title = req.form['title']
        _fin = req.form['end']
        _state = req.form['status']
        flash(json.loads(self.api.task_add(_title, _fin, _state)))
        return redirect(url_for('all_tasks_route'))

    def delete(self, req, tid):
        flash(json.loads(self.api.task_del(tid)))
        return redirect(url_for('all_tasks_route'))

    def update(self, req, tid):
        _title = req.form['title']
        _fin = req.form['end']
        _state = req.form['status']
        flash(json.loads(self.api.task_upd(tid, _title, _fin, _state)))
        return redirect(url_for('all_tasks_route'))