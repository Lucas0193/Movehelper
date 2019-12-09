from flask import url_for, current_app

from movehelper.models import UserAccount
from movehelper.config import Operations
from movehelper.helpers import generate_token
from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_login_normal_user(self):
        response = self.login()
        data = response.get_data(as_text=True)
        self.assertIn('Login success.', data)

    def test_fail_login(self):
        response = self.login(email='wrong-username@movehelper.com', pwd='wrong-password')
        data = response.get_data(as_text=True)
        self.assertIn('Invalid email or password.', data)

    def test_logout_user(self):
        self.login()
        response = self.logout()
        data = response.get_data(as_text=True)
        self.assertIn('Logout success!', data)

    def test_login_protect(self):
        response = self.client.get(url_for('user.index'), follow_redirects=True)
        data = response.get_data(as_text=True)
        #self.assertIn('Please log in to access this page.', data)

    def test_unconfirmed_user_permission(self):
        self.login(email='unconfirmed@movehelper.com', pwd='123456789')
        response = self.client.get(url_for('tasks.newtask'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Please confirm your account first.', data)


    def test_register_account(self):
        response = self.client.post(url_for('auth.register'), data=dict(
            email='test@movehelper.com',
            username='test',
            pwd='12345678',
            pwd2='12345678'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Confirm email sent, check your inbox.', data)

    def test_confirm_account(self):
        user = UserAccount.query.filter_by(email='unconfirmed@movehelper.com').first()
        self.assertFalse(user.confirmed)
        token = generate_token(user=user, operation='confirm')
        self.login(email='unconfirmed@movehelper.com', pwd='123456789')
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Account confirmed.', data)
        self.assertTrue(user.confirmed)

    def test_bad_confirm_token(self):
        self.login(email='unconfirmed@movehelper.com', pwd='123456789')
        response = self.client.get(url_for('auth.confirm', token='bad token'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Invalid or expired token.', data)
        self.assertNotIn('Account confirmed.', data)

    def test_changepassword(self):
        self.login()
        response = self.client.post(url_for('user.passwordchange'), data=dict(
            pwd='12345678',
            pwd2='12345678'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('PasswordChange successed. Please re-Login', data)