from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email

class RegisterForm(Form):
    username = TextField('Username', validators=[DataRequired('Please enter your Username')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your Password')])
    email = StringField('Email', validators=[DataRequired('Please enter your Email'), Email('Please enter a right Email address')])

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired('Please enter your user name')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password')])
    remember_me = BooleanField('Remember me', default=False)

class BlogForm(Form):
    title = StringField('title', validators=[DataRequired('Title can not be empty')])
    abstract = TextAreaField('abstract')
    body = TextAreaField('body', validators=[DataRequired('Body can not be empty')])
