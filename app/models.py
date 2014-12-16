from app import db


author_book = db.Table('author_book',
	db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
	db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)


class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), index=True)
	authors = db.relationship('Author', secondary=author_book, backref='authors')

	def __repr__(self):
		return '<Book: {}>'.format(self.title)


class Author(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), index=True)

	def __repr__(self):
		return '<Author: {}>'.format(self.name)



