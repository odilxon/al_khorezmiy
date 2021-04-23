from forms import *
from token import generate_confirmation_token, confirm_token

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



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        print("vali")
        
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.password == form.password.data:
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    print(form.errors)
    return render_template('login.html', title='Sign In errorr', form=form, errors=form.errors)
#123 

@app.route('/register', methods=['GET', 'POST'])
def register():
    data = Organisation.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(    
                        country=form.country.data, 
                        email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        username=form.username.data,
                        org_id=form.organizationid.data, 
                        phone=form.phone.data, 
                        sciencedegree=form.sciencedegree.data, 
                        user_lvl=0, 
                        confirmed=False,
                        password=form.password.data
                    )
        if form.organizationid.data not in Organisation.query.all():
            new_org = Organisation(
                name=form.organizationid.data,
                country=form.country.data)
            db.session.add(new_org)
            db.session.commit()
        db.session.add(user)
        db.session.commit()
        print('Congratulations, you are now a registered user!')
        token = generate_confirmation_token(user.email)
        return redirect(url_for('login'))
    print(form.errors)
    return render_template('register.html', title='Register', form=form, data=data)

@app.context_processor
def utility_processor():
    def Capi(name):
        return name.split(".")[0][0].upper() + name.split(".")[0][1::] #returning name of the file name wo extension and w first letter uppercase
    return dict(Capi=Capi)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/articles')
def articles():
    return render_template("articles.html")

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
@login_required
def submitarticle():
    return render_template('submitarticle.html')


@app.route('/addtemplates')
def addtemplates():
    return render_template('addtemplates.html')


@app.route('/generalsettings')
def generalsettings():
    return render_template('generalsettings.html')


@app.route('/manageuser')
def manageuser():
    return render_template('manageuser.html')


@app.route('/manageeditions')
def manageeditions():
    return render_template('manageeditions.html')


@app.route('/emailtemplates')
def emailtemplates():
    return render_template('emailtemplates.html')


@app.route('/accountsettings')
def accountsettings():
    return render_template('accountsettings.html')


@app.route("/tests")
def test():
    return "Works!"
    
@app.route("/livesearch", methods=['POST'])
def livesearch():
    searchbox = request.form.get("text")
    data = Organisation.query.all()
    lol = []
    for org in data:
        org_name = org.name.lower()
        if searchbox.lower() in org_name:
            lol.append(org.format())
    return jsonify(lol)
        


if __name__ == '__main__':
    app.run(debug=True, port=5001)

