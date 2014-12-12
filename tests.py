import os
import library
import unittest
import tempfile


class libraryTestCase(unittest.TestCase):

	def setUp(self):
		self.db_fd, library.app.config['DATABASE'] = tempfile.mkstemp()
		self.app = library.app.test_client()
		library.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(library.app.config['DATABASE'])

	def login(self, username, password):
		return self.app.post('/login', data=dict(
			username=username,
			password=password
		), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def test_login_form_present_for_guests(self):
		rv = self.app.get('/')
		assert 'Login' in rv.data

	def test_guest_can_create_account():
		rv = self.app.post('/signup', data=dict(
			username='admin',
			password='admin'
			), follow_redirects=True)
		assert 'Account has been created' in rv.data

	def test_login_logout(self):
		rv = self.login('admin', 'admin')
		assert 'You were logged in' in rv.data
		rv = self.logout()
		assert 'You were logged out' in rv.data
		rv = self.login('adminq', 'admin')
		assert 'Invalid username' in rv.data
		rv = self.login('admin', 'adminq')
		assert 'Invalid password' in rv.data

	def test_add_book(self):
		self.login('admin', 'admin')
		vr = self.app.post('/add_book', data=dict(
			title='New Book',
			author=1), follow_redirects=True)
		assert 'New Book' in vr.data
		self.logout()
		vr = self.app.post('/add_book', data=dict(
			title='New Book',
			author=1), follow_redirects=True)
		assert 'Access denine' in vr.data

	def test_user_can_edit_book(self):
		self.login('admin', 'admin')
		vr = self.app.post('/update_book', data=dict(
			id=1,
			title='New Title',
			author=1), follow_redirects=True)
		assert 'Book has been updated' in vr.data

	def test_user_can_delete_book(self):
		self.login('admin', 'admin')
		vr = self.app.post('/delete_book', data=dict(
			id=1), follow_redirects=True)
		assert 'removed' in vr.data

	def test_user_can_add_author(self):
		self.login('admin', 'admin')
		vr = self.app.post('/add_author', data=dict(
			name='Author Name'), follow_redirects=True)
		assert 'Author Name added' in vr.data

	def test_user_can_edit_author(self):
		self.login('admin', 'admin')
		vr = self.app.post('/edit_author', data=dict(
			id=1,
			name='New Name'), follow_redirects=True)
		assert 'Name changed' in vr.data

	def test_user_can_delete_author(self):
		self.login('admin', 'admin')
		vr = self.app.post('/delete_author', data=dict(
			id=1), follow_redirects=True)
		assert 'removed' in vr.data

	def test_guest_can_find_the_book_by_title(self):
		vr = self.app.get('/search?book=Book')
		assert 'New Book' in vr.data

	def test_guest_can_find_the_book_by_author(self):
		vr = self.app.get('/search?book=Name')
		assert 'New Book' in vr.data

if __name__ == '__main__':
	unittest.main()