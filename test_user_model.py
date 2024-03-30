"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import NotNullViolation

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        
        user1 = User.signup('user1test', 'ueser1test@email.com', 'user1passwordtest', None)
        user1id = 11111
        user1.id = user1id
        
        user2 = User.signup('user2test', 'ueser2test@email.com', 'user2passwordtest', None)
        user2id = 22222
        user2.id = user2id
        
        db.session.commit()
        
        self.user1 = user1
        self.user2 = user2
    
        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        
    
    #test is_following / is_followed_by features
        
    def test_user_follows(self):
        self.user1.following.append(self.user2)
        db.session.commit()
        
        #can add more users in setup to test at higher numbers
        self.assertEqual(len(self.user2.following), 0)
        self.assertEqual(len(self.user2.followers), 1)
        self.assertEqual(len(self.user1.following), 1)
        self.assertEqual(len(self.user1.followers), 0)

        #testing that ids are recognizable across users
        self.assertEqual(self.user1.following[0].id, self.user2.id)
        self.assertEqual(self.user2.followers[0].id, self.user1.id)
        
    def test_is_followed_by(self):
        self.user1.followers.append(self.user2)
        db.session.commit()
        
        self.assertTrue(self.user1.is_followed_by(self.user2))
        self.assertFalse(self.user2.is_followed_by(self.user1))
        
    # Does is_following successfully detect when user1 is following user2?
    # Does is_following successfully detect when user1 is not following user2?    
    def test_is_following(self):
        self.user1.followers.append(self.user2)
        db.session.commit()
        
        self.assertFalse(self.user1.is_following(self.user2))
        self.assertTrue(self.user2.is_following(self.user1))
              
# Does User.create successfully create a new user given valid credentials?
    def test_create_valid_user(self):
        user_test = User.signup('testname', 'testemail@email.com', 'testpassword', None)
        user_test_id = 123456
        user_test.id = user_test_id
        db.session.commit()
        
        self.assertEqual(user_test.username, 'testname')
        self.assertEqual(user_test.email, 'testemail@email.com')
        self.assertNotEqual(user_test.password, 'testpassword')
        self.assertIsNotNone(user_test)
        self.assertTrue(user_test.password.startswith('$2b$'))
        
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "", None)
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", None, None)
        
    # Testing authentication 
    
    def test_valid_authentication(self):
        user = User.authenticate(self.user1.username, 'user1passwordtest')
        
        if user:
            self.assertEqual(user.id, self.user1.id)
        else:
            self.fail("Authentication failed")
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("wrong", "user1passwordtest"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.user1.username, "wrongpassword"))