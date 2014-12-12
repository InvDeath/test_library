from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
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
