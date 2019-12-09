import unittest

from flask import url_for, current_app

from movehelper import create_app
from movehelper.tools import db
from movehelper.models import UserAccount, UserTasks, TaskOrders

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()

        # Integration testing of user authority (11/23)
        normal_user = UserAccount(id='100001', email='normal@movehelper.com', username='normal', confirmed=True, certificated=True)
        normal_user.create_password('123456789')
        unconfirmed_user = UserAccount(email='unconfirmed@movehelper.com', username='unconfirmed', confirmed=False)
        unconfirmed_user.create_password('123456789')
        uncertificated_user = UserAccount(id='100003', email='uncertificated@movehelper.com', username='uncertificated', confirmed=True, certificated=False)
        uncertificated_user.create_password('123456789')

        # Integration testing of user to operate tasks (12/1)
        normal_task = UserTasks(id='1', title='task1', context='text1', contact='contact1', location='location1', mpnum='1', user_id='100001')
        closed_task = UserTasks(id='2', title='task2', context='text2', contact='contact2', location='location2', mpnum='1', status=True, user_id='100003')
        
        # Integration testing of user to make applying and order (12/7)
        normal_order = TaskOrders(id='1',manpower='100001', task_id='2')
        uncertificated_user2 = UserAccount(email='uncertificated2@movehelper.com', username='uncertificated2', confirmed=True, certificated=False)
        uncertificated_user2.create_password('123456789')
        
        db.session.add_all([normal_user, unconfirmed_user, uncertificated_user, uncertificated_user2, normal_task, closed_task, normal_order])
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