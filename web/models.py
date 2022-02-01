from enum import unique
from . import Db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(Db.Model, UserMixin):
    id = Db.Column(Db.Integer, primary_key=True)
    isAdmin = Db.Column(Db.Boolean, default=False)
    isActive = Db.Column(Db.Boolean, default=False)
    email = Db.Column(Db.String(100), unique=True)
    firstName = Db.Column(Db.String(100))
    surname = Db.Column(Db.String(100))
    username = Db.Column(Db.String(100), unique=True)
    password = Db.Column(Db.String(100))
    creationTime = Db.Column(Db.DateTime(timezone=True), default=func.now())
