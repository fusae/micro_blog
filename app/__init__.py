from flask import Flask
from flask_wtf.csrf import CsrfProtect
import os
from flask_login import LoginManager
from config import database
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from flask_mail import Mail

client = MongoClient()
db = client[database] # database's name
csrf = CsrfProtect()
lm = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    Bootstrap(app)
    csrf.init_app(app)
    lm.init_app(app)
    lm.login_view = 'login'
    mail.init_app(app)
    
    return app

app = create_app()
from app import views, models
