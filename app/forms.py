from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(Form):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password_repeat = PasswordField(
        'password_repeat', validators=[DataRequired(), EqualTo('password')])
    email = StringField('email', validators=[DataRequired(), Email()])

class BookForm(Form):
	title = StringField('title', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])
	author = StringField('author', validators=[DataRequired()])
