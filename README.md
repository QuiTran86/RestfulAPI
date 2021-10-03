# RestfulAPI

- This is my pet project to design a restfulAPI for social network.

- Testing application locality
```console
quitran@macbook:~$ export FLASK_APP=app.py
quitran@macbook:~$ export SECRET_KEY=${SECRET_KEY}
quitran@macbook:~$ export SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_URI_TEST}
quitran@macbook:~$ export FLASK_ENV=development
```
- Deploying production
```console
quitran@macbook:~$ export FLASK_APP=app.py
quitran@macbook:~$ export SECRET_KEY=${SECRET_KEY}
quitran@macbook:~$ export SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_URI}
quitran@macbook:~$ export FLASK_ENV=production
```
