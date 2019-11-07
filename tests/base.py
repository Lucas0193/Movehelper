import unittest

from flask import url_for, current_app

from movehelper import create_app
from movehelper.tools import db
from movehelper.models import UserAccount, UserTasks

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()


        normal_user = UserAccount(email='normal@movehelper.com', username='normal', confirmed=True)
        normal_user.create_password('123456789')
        unconfirmed_user = UserAccount(email='unconfirmed@movehelper.com', username='unconfirmed', confirmed=False)
        unconfirmed_user.create_password('123456789')
       


        db.session.add_all([normal_user, unconfirmed_user])
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self, email=None, pwd=None):
        if email is None and pwd is None:
            email = 'normal@movehelper.com'
            pwd = '123456789'

        return self.client.post(url_for('auth.login'), data=dict(
            email=email,
            pwd=pwd
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)