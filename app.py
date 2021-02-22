
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)






@app.route('/', methods = ["GET"])
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')
    

@app.route('/articles')
def articles():
    return render_template('articles.html')

    
@app.route("/tests")
def test():
    return "Works"
    
if __name__ == '__main__':
    app.run(debug=True)

