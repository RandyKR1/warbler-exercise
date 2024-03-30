import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    
    def setup(self):
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()
        
        
        self.user1 = User.setup('user1', 'test1@test.com', 'password1', None)
        self.user1.id = 11111
        self.user2 = User.setup('user2', 'test2@test.com', 'password2', None)
        self.user2.id = 22222
        self.user3 = User.setup('user1', 'test3@test.com', 'password3', None)
        self.user3.id = 33333
        
        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
        
    def test_all_users(self):
        with self.client as c:
            resp = c.get('/users')
        
        self.assertIn('@user1', str(resp.data))
        self.assertIn('@user2', str(resp.data))
        self.assertIn('@user3', str(resp.data))
        
        