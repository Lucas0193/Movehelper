from flask import url_for, current_app

from movehelper.models import UserAccount, UserTasks
from movehelper.config import Operations
from movehelper.helpers import generate_token
from tests.base import BaseTestCase

class TasksTestCase(BaseTestCase):

    def test_Task_release(self):
        self.login()
        response = self.client.post(url_for('tasks.newtask'), data=dict(
            title = 'title3',
            context = 'context3',
            contact = 'contact3',
            location = 'location3',
            manpower = '1'

        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Task Created!', data)
    
    def test_Task_edit(self):
        self.login()
        response = self.client.post(url_for('tasks.taskedit', task_id='1'), data=dict(
            title = 'new',
            context = 'new',
            contact = 'new',
            location = 'new',
            manpower = '1'

        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Task Updated!', data)

    def test_Task_delete(self):
        self.login()
        response = self.client.post(url_for('tasks.taskdelete', task_id='1'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Task Deleted!', data)

   
    def test_Task_detail(self):
        self.login()
        response = self.client.post(url_for('tasks.taskdet', task_id='1'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Title:&nbsp;&nbsp;task1', data)

    def test_Task_mytasks_list(self):
        self.login()
        response = self.client.post(url_for('tasks.mytasks'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('TaskID:&nbsp;&nbsp;1', data)
    
    def test_Task_order(self):
        self.login(email='uncertificated@movehelper.com', pwd='123456789')
        response = self.client.post(url_for('tasks.applieddet', task_id='2'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('OrderID:&nbsp;&nbsp;1', data)
    
    