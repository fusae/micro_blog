from flask import Flask
from flask_wtf.csrf import CsrfProtect
import os
from flask_login import LoginManager
from config import database
from pymongo import MongoClient
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
client = MongoClient()
db = client[database] # database's name
csrf = CsrfProtect()
csrf.init_app(app)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
