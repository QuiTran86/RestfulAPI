from hashlib import md5
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ..app import db, login_manager

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('users.id')))


class Users(UserMixin, db.Model):
    about_me = db.Column(db.String(140))
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    followed = db.relationship('Users', secondary=followers,
                               primaryjoin=followers.c.follower_id,
                               secondaryjoin=followers.c.followed_id,
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
