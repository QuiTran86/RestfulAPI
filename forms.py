from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=150)])
    submit = SubmitField('Submit')

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_username(self, username):
        if username.data != self.original_name:
            from RestfulAPI.models.users import Users
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Please use an other username.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirmed Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        from .models.users import Users
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        from .models.users import Users
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email')
