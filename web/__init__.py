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
        
    from web.signInProcess.routes import signInBlueprint
    from web.resetPasswordProcess.routes import resetBlueprint
    from web.searchProcess.routes import searchBlueprint
    from web.models import User

    program.register_blueprint(searchBlueprint, url_prefix='/')
    program.register_blueprint(signInBlueprint, url_prefix='/')
    program.register_blueprint(resetBlueprint, url_prefix='/')
    createDb(program)

    siteDirectionManager = login_manager.LoginManager()
    siteDirectionManager.login_view = 'signInBlueprint.login'
    siteDirectionManager.init_app(program) 

    @siteDirectionManager.user_loader
    def getUser(id):
        return User.query.get(int(id))

    return program

def createDb(program):
    if not path.exists('web/'+database):
        Db.create_all(app=program)
