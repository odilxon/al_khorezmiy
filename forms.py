from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import *

class RegistrationForm(FlaskForm):
  firstname = StringField('Firstname', validators=[DataRequired()])
  lastname = StringField('Lastname', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  organizationid = StringField('Organization ID', validators=[DataRequired()])
  country = StringField('Country', validators=[DataRequired()])
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
      'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  sciencedegree = StringField('Science Degree', validators=[DataRequired()])
  phone = IntegerField('Phonenumber', validators=[DataRequired()])
  user_lvl = StringField('User Level', validators=[DataRequired()])
  submit = SubmitField('Register')

  def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first()
      if user is not None:
          raise ValidationError('Please use a different username.')

  def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user is not None:
          raise ValidationError('Please use a different email address.')
          
class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

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




