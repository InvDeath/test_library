from app import db


author_book = db.Table('author_book',
                       db.Column(
                           'author_id', db.Integer, db.ForeignKey('author.id')),
                       db.Column(
                           'book_id', db.Integer, db.ForeignKey('book.id'))
                       )


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    authors = db.relationship(
        'Author', secondary=author_book, backref='authors')
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Book: {}>'.format(self.title)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<Author: {}>'.format(self.name)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))

    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User: {}>'.format(self.name)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
