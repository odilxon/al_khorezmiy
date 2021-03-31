
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterationForm, LoginForm, SubmitYourArticleForm
from datetime import datetime
from flask_login import LoginManager
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '4079d33f50e34921722161947c3cab26'


posts = [
    {
        'author': 'Sherlock Holmes',
        'title': 'Blog Post 1',
        'content': 'First post',
        'datepased': 'March 24 2021'
    },
    {
        'author': 'Djhon Watson',
        'title': 'Blog Post 2',
        'content': 'Second post',
        'datepased': 'March 25 2021'
    }
]

@app.context_processor
def utility_processor():
    def Capi(name):
        return name.split(".")[0][0].upper() + name.split(".")[0][1::] #returning name of the file name wo extension and w first letter uppercase
    return dict(Capi=Capi)


@app.route('/articlelist')
def articlelist():
    return render_template('articlelist.html')


@app.route('/articledetail')
def articledetail():
    return render_template('articledetail.html')


@app.route('/issueyears')
def issueyears():
    return render_template('issueyears.html')


@app.route('/submitarticle')
def submitarticle():
    return render_template('submitarticle.html')

@app.route('/foraccount')
def foraccount():
    return render_template('foraccount.html')



@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
    if request.method == 'POST':
        if  login(request.form['username'],
                  request.form['password']):
            return user(request.form['blabla'])
        else:
            error = 'Invalid username/password'
    return render_template('foraccount.html', error=error)


    




@app.route("/tests")
def test():
    return "Works!"
    

if __name__ == '__main__':
    app.run(debug=True)

