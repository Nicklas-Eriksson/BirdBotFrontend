from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import login_manager
from sqlalchemy.sql.functions import user
from dotenv import load_dotenv

Db = SQLAlchemy()
load_dotenv()
SecretKey = os.getenv("SecretKey")
database = os.getenv("Database")

def start():
    program = Flask(__name__)
    program.config['SECRET_KEY'] = SecretKey
    program.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database}'
    Db.init_app(program)
    
    #from web.views import views
    from web.auth import auth
    from web.models import User

    #program.register_blueprint(views, url_prefix='/')
    program.register_blueprint(auth, url_prefix='/')
    createDb(program)

    siteDirectionManager = login_manager.LoginManager()
    siteDirectionManager.login_view = 'auth.login'
    siteDirectionManager.init_app(program) 

    @siteDirectionManager.user_loader
    def getUser(id):
        return User.query.get(int(id))

    return program

def createDb(program):
    if not path.exists('web/'+database):
        Db.create_all(app=program)
