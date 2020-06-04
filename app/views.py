from app import *

@app.route('/', methods=['GET'])
def index_route():
    return MainCtrl(app, get_db_info()).index()

@app.route('/register', methods=['POST'])
def registration_route():
    return AuthCtrl(app, get_db_info()).registration(request)

@app.route('/signin', methods=['POST'])
def login_route():
    return AuthCtrl(app, get_db_info()).login(request)

@app.route('/signout', methods=['POST'])
def logout_route():
    return AuthCtrl(app, get_db_info()).logout(request)

@app.route('/user', methods = ['GET'])
def dashboard_route():
    return UserCtrl(app, get_db_info()).info()

@app.route('/user/task', methods = ['GET'])
def all_tasks_route():
    return UserCtrl(app, get_db_info()).all_tasks()

@app.route('/user/task/<int:tid>', methods = ['GET'])
def one_task_route(tid):
    return UserCtrl(app, get_db_info()).get_task(tid)

@app.route('/user/task/add', methods = ['POST'])
def add_task_route():
    return TaskCtrl(app, get_db_info()).create(request)

@app.route('/user/task/<int:tid>', methods = ['POST'])
def update_task_route(tid):
    return TaskCtrl(app, get_db_info()).update(request, tid)

@app.route('/user/task/del/<int:tid>', methods = ['POST'])
def delete_task_route(tid):
    return TaskCtrl(app, get_db_info()).delete(request, tid)