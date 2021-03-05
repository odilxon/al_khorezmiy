
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)


@app.context_processor
def utility_processor():
    def Capi(name):
        return name.split(".")[0][0].upper() + name.split(".")[0][1::] #returning name of the file name wo extension and w first letter uppercase
    return dict(Capi=Capi)

@app.route('/', methods = ["GET"])
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')
    

@app.route('/articles')
def articles():
    return render_template('articles.html')

    
@app.route('/article-list')
def article_list():
    return render_template('article-list.html')


@app.route('/article-detail')
def article_detail():
    return render_template('article-detail.html')
@app.route("/tests")
def test():
    return "Works!"

if __name__ == '__main__':
    app.run(debug=True)

