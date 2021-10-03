from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import Config
from .forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sunny'}
    posts = [
        {'author': {'username': 'Tran'},
         'body': 'Temporary effort will not help us achieve success'},
        {'author': {'username': 'Susan'},
         'body': 'The beautiful day in Portland'}
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for username {form.username.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)



