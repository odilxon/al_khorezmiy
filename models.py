from flask_login import UserMixin, login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


from flask_login import LoginManager
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = '4079d33f50e34921722161947c3cab26'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    #articles = db.relationship
    
class Issues(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    release = db.Column(db.Integer, nullable=False)
    #articles = db.relationship()

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String, nullable=False)
    files = db.Column(db.String, nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'))
    status = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return '<Article %r>' %self.id