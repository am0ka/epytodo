from app import *
from app.models import *
from flask import *
from datetime import datetime

class API(object):
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.user = User(self.app, self.db)
        self.task = Task(self.app, self.db)
    
    # USER API

    def user_add(self, username, password):
        _response = {}
        if not username.isalnum():
            _response['error'] = "internal error"
        else:
            if self.user.is_registered_name(username):
                _response['error'] = "account already exists"
            else:
                if not username and not password:
                    _response['error'] = "internal error"
                else:
                    self.user.add(username, password)
                    _response['result'] = 'account created'
        return json.dumps(_response)

    def user_in(self, username, password):
        _response = {}
        if not username and not password:
            _response['error'] = "login or password does not match"
        else:
            if not self.user.is_registered_name(username):
                _response['error'] = "login or password does not match"
            elif not self.user.verify(username, password):
                _response['error'] = "login or password does not match"
            else:
                session['username'] = username
                session['id'] = self.user.get_userid(username)
                _response['result'] = "signin successful"
        return json.dumps(_response)
    
    def user_out(self):
        _response = {}
        session.pop('username', None)
        session.pop('id', None)
        _response['response'] = "signout successful"
        return json.dumps(_response)

    # TASK API

    def task_add(self, title, fin, state):
        _response = {}
        if not session['username']:
            _response['error'] = "you must be logged in"
        elif not title or "None" in title:
                _response['error'] = "internal error"
        else:
            if self.task.create(session['id'], title, fin, state):
                _response['result'] = "new task added"
            else:
                _response['error'] = "internal error"
        return json.dumps(_response)

    def task_upd(self, tid, title, fin, state):
        _response = {}
        if not session['username']:
            _response['error'] = "you must be logged in"
        elif not self.task.is_exists(tid):
            _response['error'] = "task id does not exist"
        else:
            self.task.update(tid, title, fin, state)
            _response['result'] = "update done"
        return json.dumps(_response)

    def task_del(self, tid):
        _response = {}
        if not session['username']:
            _response['error'] = "you must be logged in"
        elif not self.task.is_exists(tid):
            _response['error'] = "task id does not exist"
        else:
            if self.task.delete(tid):
                _response['result'] = "deleted"
            else:
                _response['error'] = "internal error"
        return json.dumps(_response)
    
    def select_all_tasks(self, uid):
        _response = {}
        if not self.user.is_registered_id(uid):
            _response['error'] = "user doesn't exists"
        else:
            _data = self.task.get_all_by_uid(uid)
            for i in range(len(_data)):
                if _data[i][2] and _data[i][3]:
                    _data[i][2] = datetime.strftime(_data[i][2], "%Y-%m-%d %H:%M:%S")
                    _data[i][3] = datetime.strftime(_data[i][3], "%Y-%m-%d %H:%M:%S")
            _response['result'] = _data
        return json.dumps(_response)

    def get_task(self, tid):
        _response = {}
        if not self.task.is_exists(tid):
            _response['error'] = "internal error"
        else:
            _data = self.task.get_by_id(tid)
            if not _data:
                _response['error'] = 'internal error'
            else:
                if _data[2]:
                    _data[2] = datetime.strftime(_data[2], "%Y-%m-%d %H:%M:%S")
                if _data[3]:
                    _data[3] = datetime.strftime(_data[3], "%Y-%m-%d %H:%M:%S")
                _response['result'] = _data
        return json.dumps(_response)
            