from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm


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

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('You were signed in')
		return redirect('/')

	context = {
		'form': form,
		'providers': app.config['OPENID_PROVIDERS']
	}
	return render_template('login.html', **context)
