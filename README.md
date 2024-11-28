it's a django project

start with setting up environment:

```
$ virtualenv djangoenv -p python3.13
$ pip install django
$ cd djangoenv
$ source bin/activate
```

then go to the root of git repo and do
```
$ ./manage.py runserver
```

try http://localhost:8000
