from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class RegisterationForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired(), Length(min=6, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign up')

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




