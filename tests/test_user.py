from flask import url_for, current_app

from movehelper.models import UserAccount, UserTasks, TaskOrders
from movehelper.config import Operations
from movehelper.helpers import generate_token
from tests.base import BaseTestCase

class UserTestCase(BaseTestCase):

    def test_User_certificated_permission(self):
        self.login(email='uncertificated@movehelper.com', pwd='123456789')
        response = self.client.get(url_for('user.myapply'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Please certificate your account first.', data)

    def test_User_certificated(self):
        self.login(email='uncertificated2@movehelper.com', pwd='123456789')
        response = self.client.post(url_for('user.certificate'), data=dict(
            namef = 'fname',
            namem = 'mname',
            namel = 'lname',
            birthday = '1991-01-01',
            gender = 'male',
            phone = '541111111',
            onid = '933xxxxxx',
            license = 'xxxxxxxxx'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Certification successed.', data)
    
    def test_User_certificated_protection(self):
            self.login()
            response = self.client.get(url_for('user.certificate'), follow_redirects=True)
            data = response.get_data(as_text=True)
            self.assertIn('You were already certificated!', data)
   
    
    def test_User_applytask(self):
            self.login()
            response = self.client.get(url_for('user.applytask', task_id='1'), follow_redirects=True)
            data = response.get_data(as_text=True)
            self.assertIn('You applied this task', data)

    def test_User_applytask_protection(self):
            self.login()
            response = self.client.get(url_for('user.applytask', task_id='2'), follow_redirects=True)
            data = response.get_data(as_text=True)
            self.assertIn('This task was closed', data)
    
    def test_User_myapply_list(self):
            self.login()
            response = self.client.get(url_for('user.myapply'), follow_redirects=True)
            data = response.get_data(as_text=True)
            self.assertIn('OrderNo.&nbsp;1&nbsp;&nbsp;|&nbsp;&nbsp;TaskNo.&nbsp;2', data)
