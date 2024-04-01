import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    
    def setUp(self):
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()
        
        self.test_user1 = User.signup('test_user1', 'test_user1@email.com', 'test_user_password', None)
        self.test_user1.id = 44444
        
        
        
        self.user1 = User.signup('user1', 'test1@test.com', 'password1', None)
        self.user1.id = 11111
        self.user2 = User.signup('user2', 'test2@test.com', 'password2', None)
        self.user2.id = 22222
        self.user3 = User.signup('user3', 'test3@test.com', 'password3', None)
        self.user3.id = 33333
        
        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
        
    def test_list_users(self):
        with self.client as c:
            resp = c.get('/users')
        
        self.assertIn('@user1', str(resp.data))
        self.assertIn('@user2', str(resp.data))
        self.assertIn('@user3', str(resp.data))
        
        
    def login(self, user):
        with self.client.session_transaction() as session:
            session[CURR_USER_KEY] = user.id
    
        
    def test_users_show(self):
        with self.client as c:
            self.login(self.test_user1)
        
        # Perform the GET request to the user profile page
        resp = c.get(f'/users/{self.test_user1.id}', follow_redirects=True)
        
        # Check the response status code and content
        self.assertEqual(resp.status_code, 200)
        self.assertIn('@test_user1', str(resp.data)) 
            
    def test_add_message(self):
        with self.client as c:
            self.login(self.test_user1)
            
        resp = c.get('/messages/new')
            
             