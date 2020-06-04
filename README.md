# EPyTodo
ToDo list web application written on Python Flask framework.

Frontend is mobile-first pure CSS. It has no creativity, as I didn't have any guidelines to follow.

# Prerequisites

```sh
$ cat epytodo.sql | sudo mysql -u root -p
$ virtualenv . -p /usr/bin/python3
$ source ./bin/activate
$ ./run.py
```

In order for this application to work properly, you need to create `config.py` file where you store:
```
DATABASE_NAME
DATABASE_HOST
DATABASE_SOCK
DATABASE_USER
DATABASE_PASS
```
