from app import db
from config import userCollection
import hashlib

class User:

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        # it must return str format
        # it returns bson data, so just use str() to change it to str format
        return str(db[userCollection].find_one({'email': self.email})['_id'])

    @property
    def toDict(self):
        user = {
                'username': self.username,
                'password': self.password,
                'email': self.email
                }
        return user

#class Post(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    body = db.Column(db.String(140))
#    timestamp = db.Column(db.DateTime)
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#    def __repr__(self): 
#        return '<Post %r>' % (self.body)
