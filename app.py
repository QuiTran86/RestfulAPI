from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from RestfulAPI.config import Config
from RestfulAPI.forms import LoginForm, RegisterForm, EditProfileForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

login_manager.login_view = 'login'


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changed information successfully!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.username.about_me = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


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
        from RestfulAPI.service.user_account import AccountService
        user = AccountService.is_valid_account(username=form.username.data,
                                               password=form.password.data)
        if not user:
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
        from RestfulAPI.service.user_account import AccountService
        AccountService().store_account(form.username.data, account_email=form.email.data,
                                       password=form.password.data)
        flash('Register successfully!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/reset')
def reset():
    return render_template('reset_password.html', title='Reset Password')


@app.route('/user/<username>')
@login_required
def user(username):
    from RestfulAPI.service.user_account import AccountService
    user = AccountService.get_user(username=username)
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    from RestfulAPI.service.user_account import AccountService
    AccountService().track_account(current_user)
