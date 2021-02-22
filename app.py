
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)

'''
Heroku rotates credentials periodically and updates applications where this database is attached.

Host
ec2-3-211-245-154.compute-1.amazonaws.com
Database
db0inen84vomcn
User
drtlrwvcgpljhf
Port
5432
Password
362e08830fc1e52e765f9f5390e421e962ffd396b503a4037c73f6dc72210bd1
URI
postgres://drtlrwvcgpljhf:362e08830fc1e52e765f9f5390e421e962ffd396b503a4037c73f6dc72210bd1@ec2-3-211-245-154.compute-1.amazonaws.com:5432/db0inen84vomcn
Heroku CLI
heroku pg:psql postgresql-clean-02575 --app al-khorezmiy
'''




@app.route('/', methods = ["GET"])
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')
    

@app.route('/articles')
def articles():
    return render_template('articles.html')

    
if __name__ == '__main__':
    app.run(debug=True)

