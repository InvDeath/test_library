import os
import unittest
import tempfile
from app import app, db
from config import basedir
from app.models import User, Book, Author

class appTestCase(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def create_user(self):
		user = User('admin', 'admin', 'admin@admin.com')
		db.session.add(user)
		db.session.commit()

	def create_book(self):
		self.app.post('/book_add', data=dict(
			title='New Book',
			author='auth1',
			description='Nice book!'), follow_redirects=True)

	def login(self, username, password):
		return self.app.post('/login', data=dict(
			login=username,
			password=password
		), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def test_login_form_present_for_guests(self):
		rv = self.app.get('/')
		assert 'Login' in str(rv.data)

	def test_guest_can_create_account(self):
		rv = self.app.post('/register', data=dict(
			login='admin',
			password='admin',
			password_repeat='admin',
			email='admin@mail.com'
			), follow_redirects=True)
		assert 'User sucsessfully registred' in str(rv.data)

	def test_login_logout(self):
		self.create_user()

		rv = self.login('admin', 'admin')
		assert 'You were signed in' in str(rv.data)
		rv = self.logout()
		assert 'You were logged out' in str(rv.data)
		rv = self.login('adminq', 'admin')
		assert 'Incorrect login or password' in str(rv.data)
		rv = self.login('admin', 'adminq')
		assert 'Incorrect login or password' in str(rv.data)

	def test_add_book(self):
		self.create_user()
		self.login('admin', 'admin')

		rv = self.app.post('/book_add', data=dict(
			title='New Book',
			author='auth1',
			description='Nice book!'), follow_redirects=True)
		assert 'Book added successfully' in str(rv.data)
		self.logout()
		rv = self.app.post('/book_add', data=dict(
			title='New Book',
			author='some aouthor',
			description='test'), follow_redirects=True)
		assert 'Please log in to access this page.' in str(rv.data)

	def test_user_can_edit_book(self):
		self.create_user()
		self.login('admin', 'admin')
		self.create_book()

		rv = self.app.post('/book_edit/1', data=dict(
			title='New Title',
			description='some new text',
			author=1), follow_redirects=True)
		assert 'Book has been updated' in str(rv.data)

	def test_user_can_delete_book(self):
		self.create_user()
		self.login('admin', 'admin')
		self.create_book()
		rv = self.app.get('/book_delete/1', follow_redirects=True)
		assert 'Book has been deleted' in str(rv.data)

	def test_user_can_add_author(self):
		self.login('admin', 'admin')
		rv = self.app.post('/add_author', data=dict(
			name='Author Name'), follow_redirects=True)
		assert 'Author Name added' in str(rv.data)

	def test_user_can_edit_author(self):
		self.login('admin', 'admin')
		rv = self.app.post('/edit_author', data=dict(
			id=1,
			name='New Name'), follow_redirects=True)
		assert 'Name changed' in str(rv.data)

	def test_user_can_delete_author(self):
		self.login('admin', 'admin')
		rv = self.app.post('/delete_author', data=dict(
			id=1), follow_redirects=True)
		assert 'removed' in str(rv.data)

	def test_guest_can_find_the_book_by_title(self):
		rv = self.app.get('/search?book=Book')
		assert 'New Book' in str(rv.data)

	def test_guest_can_find_the_book_by_author(self):
		rv = self.app.get('/search?book=Name')
		assert 'New Book' in str(rv.data)

	def test_cant_edit_or_delete_unexisted_book(self):
		pass

if __name__ == '__main__':
	unittest.main()