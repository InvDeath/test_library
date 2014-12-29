from flask import render_template, flash, redirect, url_for, g, session, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm, db
from .forms import LoginForm, RegisterForm, BookForm, AuthorForm, SearchForm
from .models import User, Book, Author


@app.route('/')
def index():
    books = Book.query.all()
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
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
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
    g.search_form = SearchForm()

@app.route('/book_add', methods=['GET', 'POST'])
@login_required
def book_add():
    form = BookForm()
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('book_edit.html', form=form, action='Add')

    title = request.form['title']
    description = request.form['description']
    author_name = request.form['author']

    author = Author.query.filter_by(name=author_name).first()

    if not author:
        author = Author(name=author_name)

    book = Book(title=title, authors=[author], description=description)

    db.session.add(book)
    db.session.commit()

    flash('Book added successfully', 'success')
    return redirect(url_for('index'))

@app.route('/book_edit/<id>', methods=['GET', 'POST'])
@login_required
def book_edit(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('book_edit.html', form=form, action='Edit')

    form.populate_obj(book)
    db.session.commit()
    flash('Book has been updated', 'success')
    return redirect(url_for('index'))

@app.route('/book_delete/<id>')
@login_required
def book_delete(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()

    flash('Book has been deleted', 'success')
    return redirect(url_for('index'))

@app.route('/author_add', methods=['GET', 'POST'])
@login_required
def author_add():
    form = AuthorForm()
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('author_edit.html', form=form, action='Add')
    name = request.form['name']

    author = Author(name=name)

    db.session.add(author)
    db.session.commit()

    flash('Author added successfully', 'success')
    return redirect(url_for('index'))

@app.route('/author_edit/<id>', methods=['GET', 'POST'])
@login_required
def author_edit(id):
    author = Author.query.get_or_404(id)
    form = AuthorForm(obj=author)
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('author_edit.html', form=form, action='Edit')

    form.populate_obj(author)
    db.session.commit()
    flash('Author has been updated', 'success')
    return redirect(url_for('index'))

@app.route('/author_delete/<id>')
@login_required
def author_delete(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()

    flash('Author has been deleted', 'success')
    return redirect(url_for('index'))

@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/authors')
def authors():
    authors = Author.query.all()
    return render_template('index.html', authors=authors)

@app.route('/search_result')
def search_result():
    return 'search results'