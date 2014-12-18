from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    login = StringField('login', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class RegisterForm(Form):
    login = StringField('login', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    password_repeat = StringField(
        'password_repeat', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
