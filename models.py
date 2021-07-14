from flask_login import UserMixin, login_required, current_user, login_user, logout_user, LoginManager
from flask_security.core import RoleMixin
from werkzeug.exceptions import default_exceptions
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from flask import Flask, Markup, flash, render_template, url_for, request, redirect, jsonify, abort, send_file, send_from_directory, safe_join
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, Serializer

from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join
from flask_user import roles_required, roles_accepted, user_manager
from flask_migrate import Migrate, MigrateCommand, Manager
from flask_security import SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore, Security, current_user

from flask_user import roles_accepted
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
oauth = OAuth(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
app.config['SECRET_KEY'] = '4079d33f50e3492uig172216ghjkfd1947c3cab26'
app.config['SECURITY_PASSWORD_SALT'] = 'hpqohang;jgbiu2ug5t23bl4vrqwy'

app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']= '6Ldz8HcbAAAAADnc4uu76JZ7wqL7TC8UchuYV57E'
app.config['RECAPTCHA_PRIVATE_KEY']='6Ldz8HcbAAAAACKEmYvWgj1bWkIltQ3vRedmpjMF'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin,  RoleMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    usfield = db.Column(db.Integer, db.ForeignKey('field.id'))

    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String, nullable=True)
    sciencedegree = db.Column(db.String, nullable=False)
    user_lvl = db.Column(db.String, nullable=False)
    phone = db.Column(db.String(30), nullable=False)


    articles = db.relationship("Article", backref="user", lazy=True)
    user_fields = db.relationship("Field", backref="user", lazy=True)
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
            "usfield": self.usfield,
        }
    def is_admin(self):
        print("is admin works")
        try:
            l = self.user_lvl
            if int(l) == 100:
                return True
            else:
                return False
        except Exception:
            return False

    def is_editor(self):
        print('lvl 1 kuu')
        try:
            l = self.user_lvl
            if int(l) == 10 or int(l) == 100:
                return True
        except Exception:
            pass
        return False

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user.id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return '<User %r>' % self.email

# class UserRoles(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Issue(db.Model, UserMixin):
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

class Article(db.Model, UserMixin):
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


class Organisation(db.Model, UserMixin):
    __tablename__ = 'organisation'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)

    users = db.relationship("User", backref="organisatoin", lazy=True)
    def __repr__(self):
        return self.name

    def format(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "country" : self.country,
        }


class Userfield(db.Model, UserMixin):
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

class Field(db.Model, UserMixin):
    __tablename__ = 'field'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    users = db.relationship("Userfield", backref="field", lazy=True)

    # users = db.relationship("User", backref="usernamefield", lazy=True)
    def __repr__(self):
        return self.name    

    def format(self):
        return {
            "id" : self.id,
            "name" : self.name,
        }


class Category(db.Model, UserMixin):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    paper_category = db.relationship("Paper", backref="category", lazy=True)

    def format(self):
        return {
            "id" : self.id,
            "name" : self.name,
        }



class Paper(db.Model, UserMixin):
    __tablename__ = 'paper'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String, nullable=False)
    abstract = db.Column(db.String, nullable=False)
    keyword = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    reference = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    paper_status = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    paper_actions = db.relationship("Paper_action", backref='paper', lazy=True)
    paper_statistics = db.relationship("Paper_statistic", backref='paper', lazy=True)
    
    def format(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "title" : self.title,
            "abstract" : self.abstract,
            "keyword" : self.keyword,
            "body" : self.body,
            "reference" : self.reference,
            "created_time" : self.created_time,
            "updated_time" : self.updated_time,
            "paper_status" : self.paper_status,
        }

class Score(db.Model, UserMixin):
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

class Fault(db.Model, UserMixin):
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

class Paper_action(db.Model, UserMixin):
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
            #"receiver_id" : self.receiver_id,
            "report_text" : self.report_text,
            "action_status" : self.action_status,
        }

class Paper_statistic(db.Model, UserMixin):
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


# class AdminView(ModelView):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.static_folder = 'static'

#     def is_accessible(self):
#         return session.get('user') == 'Administrator'

#     def inaccessible_callback(self, name, **kwargs):
#         if not self.is_accessible():
#             return redirect(url_for('home', next=request.url))

# class User(ModelView):
#     column_exclude_list = ['password']


# admin = Admin(votr, name='Dashboard', index_view=AdminView(Topics, db.session, url='/admin', endpoint='admin'))

# class AdminView(ModelView):
#     def is_accessible(self):
#         return current_user.has_role('admin')
    
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect( url_for('security.login', next=request.url))



# class MyModelView(ModelView):
#     def is_accessible(self):
#         print("Qachon tugiidiii yoo mayoo")
#         return current_user.is_authenticated()

#     def inaccessible_callback(self, name, **kwargs):
#         # redirect to login page if user doesn't have access
#         return redirect(url_for('login.html', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        print('I am hereeeee')
        return current_user.is_authenticated and str(current_user.user.lvl) == 100

user_manager = ModelView(User, db.session)


class MyView(ModelView):
    def _user_formatter(view, context, model, name):
        print(model)
        if model.body:
           markupstring = "<a href='/%s'>%s</a>" % (model.body, str(model.body).split('/')[-1])
           return Markup(markupstring)
        else:
           return ""

    column_formatters = {
        'body': _user_formatter
    }


admin = Admin(app,  template_mode='bootstrap4')
admin.add_view(ModelView(User, db.session))
admin.add_view(MyView(Paper, db.session))



# import enum

# class Roles(enum.Enum):
#     ADMIN = 100
#     EDITOR = 50
#     USER = 1
    