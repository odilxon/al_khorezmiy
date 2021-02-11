from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    
class Issues(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    release = db.Column(db.Integer, nullable=False)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    content = db.Column(db.String, nullable=False)
    files = db.Column(db.String, nullable=False)
    issue_id = db.Column(db.Integer, ForeignKey('issues.id'))
    status = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return '<Article %r>' %self.id
