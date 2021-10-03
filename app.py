from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from .config import Config
from .forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

login_manager.login_view = 'login'


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {'author': {'username': 'Tran'},
         'body': 'Temporary effort will not help us achieve success'},
        {'author': {'username': 'Susan'},
         'body': 'The beautiful day in Portland'}
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Import here to avoid circular import
        from .models.users import Users
        user = Users.query.filter_by(username=form.username.data).first()
        if not (user and user.check_password(form.password.data)):
            flash(f'Username or password is invalid, please check again!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        from .models.users import Users
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Register successfully!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/reset')
def reset():
    return render_template('reset_password.html', title='Reset Password')
