from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, Email

class RegisterForm(Form):
    username = TextField('username', validators=[DataRequired('Please enter your user name')])
    password = PasswordField('password', validators=[DataRequired('Please enter your password')])
    email = StringField('email', validators=[DataRequired('Please enter your email'), Email('Please enter a right email address')])
    submit = SubmitField('submit')

class LoginForm(Form):
    username = TextField('username', validators=[DataRequired('Please enter your user name')])
    password = PasswordField('password', validators=[DataRequired('Please enter your password')])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('submit')
