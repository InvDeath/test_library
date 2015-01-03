from app import app, db
from app.models import Book, Author, User

book = Book(
	id=1,
	title='Mastering Python Regular Expressions',
	description='This book is aimed at Python developers who want to learn how to leverage Regular Expressions in Python. Basic knowledge of Python is required for a better understanding.',
	authors=[Author(id=1, name='Félix López'), Author(id=2, name='Víctor Romero')]
	)
db.session.add(book)

book = Book(
	id=2,
	title='Python in Practice',
	description='This book is aimed at existing Python programmers who want to take their Python programming to the next level.',
	authors=[Author(id=3, name='Mark Summerfield')]
	)
db.session.add(book)

book = Book(
	id=3,
	title='Python Geospatial Development - Second Edition',
	description='Learn to build sophisticated mapping applications from scratch using Python tools for geospatial development.',
	authors=[Author(id=4, name='Erik Westra')]
	)
db.session.add(book)

user = User(id=1, login='admin', password='admin', email='admin@admin.com')
db.session.add(user)

db.session.commit()
