from app.controllers import *
from app.db_manager import DBManager
from flask import *
import pymysql as sql
import os
from datetime import datetime


app = Flask(__name__)
app.config.from_object('config')

connection = DBManager(app)

def get_db_info():
    return connection.get_conn()

@app.template_filter('datetime')
def format_datetime(value):
    if value:
        value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        value = value.strftime("%Y-%m-%dT%H:%M:%S")
    return value

@app.template_filter('autoversion')
def autoversion_filter(filename):
  # determining fullpath might be project specific
  fullpath = os.path.join('app/', filename[1:])
  try:
      timestamp = str(os.path.getmtime(fullpath))
  except OSError:
      return filename
  newfilename = "{0}?v={1}".format(filename, timestamp)
  return newfilename