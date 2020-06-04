from app import *
import pymysql as sql

class DBManager(object):
    def __init__(self, app):
        self.app = app
        self.db = None
        self.set_conn(app.config)

    def set_conn(self, config):
        try:
            if config['DATABASE_SOCK']:
                self.db = sql.connect(unix=config['DATABASE_SOCK'],
                                      user=config['DATABASE_USER'],
                                      password=config['DATABASE_PASS'],
                                      db=config['DATABASE_NAME'])
            else:
                self.db = sql.connect(host=config['DATABASE_HOST'],
                                      user=config['DATABASE_USER'],
                                      password=config['DATABASE_PASS'],
                                      db=config['DATABASE_NAME'])
            if self.db == None:
                raise Exception
        except Exception as error:
            print(error)
            exit(84)

    def get_conn(self):
        return self.db
