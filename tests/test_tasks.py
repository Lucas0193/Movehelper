from flask import url_for, current_app

from movehelper.models import UserAccount, UserTasks
from movehelper.config import Operations
from movehelper.helpers import generate_token
from tests.base import BaseTestCase

class TasksTestCase(BaseTestCase):
    
    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Home', data)
        self.assertIn('MoveHelper', data)
        self.assertIn('Login and rlease new announcement!', data)

   
        
