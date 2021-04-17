from flask_login import UserMixin, login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse


from flask import Flask, flash, render_template, url_for, request, redirect, jsonify


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


from flask_login import LoginManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = '4079d33f50e3492uig172216ghjkfd1947c3cab26'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String, nullable=True)
    sciencedegree = db.Column(db.String, nullable=False)
    user_lvl = db.Column(db.Integer, default=0, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    articles = db.relationship("Article", backref="user", lazy=True)
    user_fields = db.relationship("Userfield", backref="user", lazy=True)
    papers = db.relationship("Paper", backref="user", lazy=True)
    paper_actions = db.relationship("Paper_action", backref="user", lazy=True)

    def format(self):
        return {
            "id" : self.id,
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "email" : self.email,
            "org_id" : self.org_id,
            "username" : self.username,
            "password" : self.password,
            "country" : self.country,
            "sciencedegree" : self.sciencedegree,
            "user_lvl" : self.user_lvl,
            "phone" : self.phone,
        }
    
class Issue(db.Model):
    __tablename__ = 'issue'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    release = db.Column(db.Integer, nullable=False)
    articles = db.relationship("Article", backref="issue", lazy=True)

    def format(self):
        return {
            "id" : self.id,
            "date" : self.date,
            "release" : self.release,
        }

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String, nullable=False)
    file = db.Column(db.String, nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    status = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Article %r>' %self.id

    def format(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "content" : self.content,
            "file" : self.file,
            "issue_id" : self.issue_id,
            "status" : self.status,
            "category" : self.category,
        }


class Organisation(db.Model):
    __tablename__ = 'organisation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    users = db.relationship("User", backref="organisatoin", lazy=True)

    def format(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "country" : self.country,
        }

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    paper_categories = db.relationship("Paper_category", backref="category", lazy=True)

    def format(self):
        return {
            "id" : self.id,
            "name" : self.name,
        }

class Userfield(db.Model):
    __tablename__ = 'userfield'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'))

    def format(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "field_id" : self.field_id,
        }

class Field(db.Model):
    __tablename__ = 'field'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    userfields = db.relationship("Userfield", backref="field", lazy=True)

    def format(self):
        return {
            "id" : self.id,
            "name" : self.name,
        }


class Paper_category(db.Model):
    __tablename__ = 'paper_category'
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def format(self):
        return {
            "id" : self.id,
            "paper_id" : self.paper_id,
            "category_id" : self.category_id,
        }

class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    fault_id = db.Column(db.Integer, db.ForeignKey('fault.id'))
    score_time = db.Column(db.DateTime, nullable=False)
    paper_action_id = db.Column(db.Integer, db.ForeignKey('paper_action.id'))

    def format(self):
        return {
            "id" : self.id,
            "fault_id" : self.fault_id,
            "score_time" : self.score_time,
            "paper_action_id" : self.paper_action_id,
        }

class Paper(db.Model):
    __tablename__ = 'paper'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String, nullable=False)
    abstract = db.Column(db.String, nullable=False)
    keyword = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    referance = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    paper_status = db.Column(db.String, nullable=False)
    paper_actions = db.relationship("Paper_action", backref='paper', lazy=True)
    paper_statistics = db.relationship("Paper_statistic", backref='paper', lazy=True)
    paper_categories = db.relationship("Paper_category", backref='paper', lazy=True)

    def format(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "title" : self.title,
            "abstract" : self.abstract,
            "keyword" : self.keyword,
            "body" : self.body,
            "referance" : self.referance,
            "created_time" : self.created_time,
            "updated_time" : self.updated_time,
            "paper_status" : self.paper_status,
        }




class Fault(db.Model):
    __tablename__ = 'fault'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    fault_lvl = db.Column(db.Integer, nullable=False)
    scores = db.relationship("Score", backref="fault", lazy=True)

    def format(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "fault_lvl" : self.fault_lvl,
        }

class Paper_action(db.Model):
    __tablename__ = 'paper_action'
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'))
    action_type = db.Column(db.String, nullable=False)
    action_time = db.Column(db.DateTime, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    report_text = db.Column(db.String, nullable=False)
    action_status = db.Column(db.String, nullable=False)
    scores = db.relationship("Score", backref="paper_action", lazy=True)

    def format(self):
        return {
            "id" : self.id,
            "paper_id" : self.paper_id,
            "action_type" : self.action_type,
            "action_time" : self.action_time,
            "sender_id" : self.sender_id,
            "receiver_id" : self.receiver_id,
            "report_text" : self.report_text,
            "action_status" : self.action_status,
        }

class Paper_statistic(db.Model):
    __tablename__ = 'paper_statistic'
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'))
    type = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    ip_adress = db.Column(db.String, nullable=False)

    def format(self):
        return {
            "id" : self.id,
            "paper_id" : self.paper_id,
            "type" : self.type,
            "date" : self.date
        }
'''
def GetToken():
    Usr = User.query.all()
    id = None
    if len(Usr) == 0:
        Usr = User(name="Usr1", login="Usr1", password="Usr1", info="Info", RFID="A76F773C", depart_id=Dp.id)
        db.session.add(Usr)
        db.session.commit()
        Usr = User.query.first()
        id = Usr.id
    token = jwt.encode({'public_id': id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=3600)}, app.config['SECRET_KEY'], algorithm="HS256") 
    return jsonify({"msg": "Success", "token": token})
'''
