from flask import Flask
import os
from flask_login import LoginManager
from config import database
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config')
client = MongoClient()
db = client[database] # database's name


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
