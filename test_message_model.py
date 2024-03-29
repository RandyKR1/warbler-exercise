#    python -m unittest test_message_model.py


"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

# this sets the DATABASE_URL variable to point to warbler_test
os.environ['DATABASE_URL'] = "postgresql:///warbler_test" 


from app import app


db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        
        #drop and recreate tables in warbler_test db
        db.drop_all()
        db.create_all()

        # assigning the testing user id, an arbitrary number to represent the user
        self.uid = 94566
        
        u = User.signup("testing", "testing@test.com", "password", None)
        u.id = self.uid
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):
        """Does basic model work?"""
        
        m = Message(
            text="my test message",
            user_id=self.uid
        )

        db.session.add(m)
        db.session.commit()

        user = User.query.get(self.uid)

        # User should have 1 message
        self.assertEqual(len(user.messages), 1)
        self.assertEqual(user.messages[0].text, "my test message")