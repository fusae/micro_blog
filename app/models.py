from app import db
from config import userCollection
import hashlib
from datetime import datetime

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

class Post:
    salt = 'YJY'
    def __init__(self, title, abstract, content):
        
        self.title = title
        self.abstract = abstract
        self.content = content
        self.created_at = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        # use title and created time to form the hash id
        self.blog_id = hashlib.md5((Post.salt + self.created_at).encode('utf-8')).hexdigest()

    @property
    def toDict(self):
        post = {
                'title': self.title,
                'abstract': self.abstract,
                'content': self.content,
                'created_at': self.created_at,
                'blog_id': self.blog_id
                }
        return post


