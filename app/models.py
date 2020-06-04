from app import *
from flask import *
import hashlib
from datetime import datetime

class User(object):
    def __init__(self, app, db):
        self.app = app
        self.db = db
    
    def is_registered_name(self, username):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT COUNT(1) FROM user WHERE username = '%s'" %
                (username))
            is_registered = cursor.fetchone()[0]
            cursor.close()
            return True if is_registered else False
        except Exception as error:
            print(error)
            return True
        return True

    def is_registered_id(self, userid):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT COUNT(1) FROM user WHERE user_id = '%s'" %
                (userid))
            is_registered = cursor.fetchone()[0]
            cursor.close()
            return True if is_registered else False
        except Exception as error:
            print(error)
            return True
        return True

    def add(self, username, password):
        try:
            _passwd = hashlib.sha512()
            _passwd.update(password.encode())
            _passwd = _passwd.hexdigest()
            cursor = self.db.cursor()
            cursor.execute\
                ("INSERT INTO user (username, password) VALUES ('%s', '%s')" %
                (username, _passwd))
            self.db.commit()
            cursor.close()
        except Exception as error:
            print(error)

    def get_userid(self, username):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT user_id FROM user WHERE username = '%s'" %
            (username))
            _userid = cursor.fetchone()[0]
            cursor.close()
            return _userid
        except Exception as error:
            print(error)
            return -1
        return -1

    def verify(self, username, password):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT password FROM user WHERE username = '%s'" %
            (username))
            _db_passwd = cursor.fetchone()[0]
            cursor.close()
            _passwd = hashlib.sha512()
            _passwd.update(password.encode())
            _passwd = _passwd.hexdigest()
            return True if _passwd == _db_passwd else False
        except Exception as error:
            print(error)
            return False
        return False

class Task(object):
    def __init__(self, app, db):
        self.app = app
        self.db = db
    
    def create(self, uid, title, fin, state):
        uid = int(uid)
        try:
            try:
                datetime.strptime(fin, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            except:
                datetime.strptime(fin, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
            with self.db.cursor() as cursor:
                if fin:
                    cursor.execute("INSERT INTO task (`title`, `status`, `end`) \
                    VALUES ('%s', '%s', '%s')" % (title, state, fin))
                elif not fin:
                    cursor.execute("INSERT INTO task (`title`, `status`, `end`) \
                    VALUES ('%s', '%s', NULL)" % (title, state))
                tid = cursor.lastrowid
                if not tid:
                    return False
                cursor.execute("INSERT INTO user_has_task (`fk_user_id`, `fk_task_id`) \
                    VALUES (%d, %d)" % (uid, tid))
                cursor.close()
            self.db.commit()
        except Exception as error:
            print(error)
            return False
        return True

    def delete(self, tid):
        tid = int(tid)
        try:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT COUNT(1) FROM user_has_task \
                    WHERE fk_task_id = '%d' AND fk_user_id = '%d'" % (tid, session['id']))
                _response = cursor.fetchone()[0]
                if _response != 1:
                    cursor.close()
                    return False
                cursor.execute("DELETE FROM user_has_task WHERE fk_task_id = '%d' \
                    AND fk_user_id = '%d'" % (tid, session['id']))
                self.db.commit()
                cursor.execute("DELETE FROM task WHERE task_id = %d" % (tid))
                cursor.close()
            self.db.commit()
        except Exception as error:
            print(error)
            return False
        return True

    def update(self, tid, title, fin, state):
        try:
            if title and state and fin:
                try:
                    _fin = datetime.strptime(fin, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                except:
                    _fin = datetime.strptime(fin, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
                self.db.cursor().execute("UPDATE task SET title = '%s', \
                    end = '%s', status = '%s' WHERE task_id = %d"
                    % (title, _fin, state, tid))
            elif title and state and not fin:
                self.db.cursor().execute("UPDATE task SET title = '%s', \
                    status = '%s' WHERE task_id = %d" % (title, state, tid))
            self.db.commit()
            self.db.cursor().close()
        except Exception as error:
            print(error)
    
    def is_exists(self, tid):
        try:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT COUNT(1) FROM task WHERE task_id = %d"
                    % (tid))
                _exists = cursor.fetchone()[0]
                cursor.close()
                return True if _exists else False
        except Exception as error:
            print(error)
        return True

    def get_by_id(self, tid):
        try:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT * FROM task WHERE task_id = %d" % (tid))
                _task = list(cursor.fetchall()[0])
                cursor.close()
                return _task
        except Exception as error:
            print(error)
        return None
    
    def get_all_by_uid(self, uid):
        _tasks = []
        try:
            with self.db.cursor() as cursor:
                cursor.execute("SELECT fk_task_id FROM user_has_task \
                    WHERE fk_user_id = %d" % (uid))
                _tids = list(cursor.fetchall())
                for tid in _tids:
                    cursor.execute("SELECT * FROM task WHERE task_id = %d" % (tid[0]))
                    _task = list(cursor.fetchall()[0])
                    _tasks.append(_task)
                cursor.close()
            return _tasks
        except Exception as error:
            print(error)
        return _tasks