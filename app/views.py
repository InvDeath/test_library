from flask import render_template, flash, redirect, url_for, g, session, request
from flask.ext.login import login_user, logout_user, current_user
from app import app, lm, db
from .forms import LoginForm, RegisterForm
from .models import User


@app.route('/')
def index():
    books = [
        {
            'title': 'book1',
            'id': 1,
            'author':
            {
                'id': 1,
                'name': 'auth1'
            }
        },
        {
            'title': 'book2',
            'id': 2,
            'author':
            {
                'id': 1,
                'name': 'auth1'
            }
        },
        {
            'title': 'book3',
            'id': 3,
            'author':
            {
                'id': 2,
                'name': 'auth2'
            }
        },
    ]
    return render_template('index.html', books=books)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('register.html', form=form)

    user = User(
        request.form['login'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User sucsessfully registred', 'success')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('login.html', form=form)

    login = request.form['login']
    password = request.form['password']

    registred_user = User.query.filter_by(
        login=login, password=password).first()

    if registred_user is None:
        flash('Incorrect login or password', 'alert')
        return redirect(url_for('login'))

    login_user(registred_user)
    flash('You were signed in', 'success')
    return redirect('/')


@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out', 'info')
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

