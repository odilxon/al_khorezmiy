from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import *
import json, re
or_ch = [(x.id, x.name) for x in Organisation.query.filter(Organisation.name != "Administration").all()]

def Get_C():
    a = []
    with open('country.json') as f:
        a = json.load(f)
    data = [(x,x) for x in a]
    return data

class RegistrationForm(FlaskForm):

    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=3, max=16, message='*Firstname not true')])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=3, max=16, message='*Lastname not true')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # email1 = StringField('Email', validators=[DataRequired(), Email()])
    organizationid = StringField('Organization ID', validators=[DataRequired()])
    country = SelectField('Country',choices=Get_C(), validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16, message='*Password need minimum 8 characters!')])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    sciencedegree = StringField('Science Degree', validators=[DataRequired()])
    phone = IntegerField('Phonenumber', validators=[DataRequired()])
    tos = BooleanField('tos',validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
    
        user = User.query.filter_by(email=email.data).first()
        
        if user is not None:
            raise ValidationError('Please use a different email address.')
          

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. you must register first', 'warning')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16, message='*Password need minimum 8 characters!')])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')   

class PapersForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    abstract = StringField('Abstract', validators=[DataRequired()])
    keyword = StringField('Keyword', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    reterence = StringField('Reterence', validators=[DataRequired()])
    createdtime = TimeField('Created Time', validators=[DataRequired()])
    updatedtime = TimeField('Updated Time', validators=[DataRequired()])
    

class SubmitYourArticleForm(FlaskForm):
    submit = SubmitField('SubmitYourArticle')

# class SubmitNow(FlaskForm):
#   submitNow = SubmitField('Submit Now')

# class ApllyFilter(FlaskForm):
#   applyFilter = SubmitField('Apply Filter')

# class ResetAll(FlaskForm):
#   resetAll = SubmitField('Reset All')

# class Addbtn(FlaskForm):
#   addbtn = SubmitField('Add btn')

# class Adddelbtn(FlaskForm):
#   adddelbtn = SubmitField('Delete btn')




