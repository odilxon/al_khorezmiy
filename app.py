from api import *
from hashlib import sha256


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        print("vali")
        
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Email is invalid', 'error')
            return redirect(url_for('login'))
        if user.password != form.password.data:
            flash('Password is invalid', 'error')
            return redirect(url_for('login'))
        if not user.confirmed:
            flash('Please confirm email before login', 'warning')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    print(form.errors)
    return render_template('login.html', title='Sign In errorr', form=form, errors=form.errors)
    

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
                        password=form.password.data,
                        usfield=form.usfieldsname.data
                    )
        if form.organizationid.data not in Organisation.query.all():
            new_org = Organisation(
                name=form.organizationid.data,
                country=form.country.data)
            db.session.add(new_org)
            db.session.commit()


        if form.usfieldsname.data not in Field.query.all():
            new_field = Field(
                name=form.usfieldsname.data)
            db.session.add(new_field)
            db.session.commit()


        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! Check Email to confirm account', 'success')
        token = generate_confirmation_token(form.email.data)
        s = request.host_url + "confirm/" + token
        st, msg = Send_EMAIL(form.email.data, f"Congratulations, you are now a registered user! confirm account {s}", title='Register your account on Al-Khorezmi')
        
        return redirect(url_for('login'))
    print(form.errors)
    return render_template('register.html', form=form, data=data)


def get_reset_token(self, expiration=1800):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        return s.dumps({'user_id': self.id}).decode('utf-8')


@app.route('/forgotpassemail', methods=['GET', 'POST'])
def forgotpassemail():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
        flash('You are welcome', 'success')
    form = RequestResetForm()
    if request.method=='POST':      
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                flash('User not found', 'error')
                return render_template('forgotpassemail.html', form=form)        
            # Funksiya to send reset link
            token = generate_confirmation_token(form.email.data)
            s = request.host_url + "resetpassword/" + token
            st, msg = Send_EMAIL(form.email.data, f"You can do this by clicking below {s}", title='Reset your Al-Khorezmi account Password')

            flash('Reset password link was sent to Email', 'success')
            return render_template('forgotpassemail.html', form=form)
        flash('Email is incorrect', 'error')
        return render_template('forgotpassemail.html', form=form)
    return render_template('forgotpassemail.html', form=form)
    
    
@app.route('/resetpassword/<string:token>', methods=['GET', 'POST'])
def resetpassword(token):
    print(token)
    if request.method == "POST":
        print('post')
        form = ResetPasswordForm()
        if form.validate_on_submit():
            new_password = request.form.get("password")
            email = confirm_token(token)
            user = User.query.filter_by(email=email).first_or_404()
            print('first or 404')
            if user.password == new_password:
                flash('Type another password', 'error')
                return render_template('resetpassword.html', form=form)            
            user.password = new_password
            db.session.commit()
            flash('Now you changed your Password', 'success')
            return redirect(url_for('login'))            
        else:
            print(form.errors)
            return render_template('resetpassword.html', form=form)
    try:
        email = confirm_token(token)
        print(email)
        if email:
            user = User.query.filter_by(email=email).first_or_404()
            print(user)
            form = ResetPasswordForm()
            return render_template('resetpassword.html', form=form)
    except:
        pass
    abort(404)
    




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

@app.route('/submitarticle')
def submitarticle():
    return render_template("submitarticle.html")

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


# @app.route('/submitarticle')
# def submitarticle():
#     return render_template('submitarticle.html')


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
        
@app.route("/livesearch_field", methods=['POST'])
def livesearch_field():
    searchbox = request.form.get("text")
    data = Field.query.all()
    lol_1 = []
    for org_1 in data:
        usfield = org_1.name.lower()
        if searchbox.lower() in usfield:
            lol_1.append(org_1.format())
    return jsonify(lol_1)




if __name__ == '__main__':
    app.run(debug=True, port=5000)

