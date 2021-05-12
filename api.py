
from forms import *
from flask import jsonify, redirect, url_for
from flask_mail import Mail, Message

from itsdangerous import URLSafeTimedSerializer, SignatureExpired


app.config["MAIL_SERVER"] = "server2.ahost.uz"
app.config["MAIL_PORT"] = 465
#app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USERNAME"] = 'odya@ladymarykay.uz'
app.config["MAIL_PASSWORD"] = 'Odilxon030101!'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@ladymarykay.uz'

mail = Mail(app)


@app.route('/admin/dashboard')    # @route() must always be the outer-most decorator
@roles_required('Admin')
def admin_dashboard():
    pass

@app.route("/api", methods=["GET"])
def main_api():
    s = request.host_url + "confirm/" + token
    return jsonify({"msg" : "Hello World"})

@app.route("/api/user", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        data = request.form
        Usr = User(name=data["name"],
            email=data["email"],
            login=data["login"],
            password=data["password"],
            org_id=data["org_id"],
            google_in=data["google_in"],
            scolar_degree=data["scolar_degree"],
            user_lvl=data["user_lvl"],
            phone=data["phone"],
            usfield=data["usfield"],
        )
        try:
            db.session.add(Usr)
            db.session.commit()
        except Exception as E:
            return jsonify({"msg" : str(E)}), 400
        return jsonify({"msg" : "Success"}), 200
    else:
        if request.args.get('org_id') is not None:
            org_id = request.args.get('org_id')
            data = db.session.query(User, Organisation.name).filter_by(org_id=org_id).join(Organisation, Organisation.id==User.org_id).all()
        else:
            data = db.session.query(User, Organisation.name).join(Organisation, Organisation.id==User.org_id).all()
        d = []
        for user, g_n in data:
            usr = user.format()
            usr["org_name"] = g_n
            d.append(usr)
        return jsonify(d)

        if request.args.get('usfield') is not None:
            usfield = request.args.get('usfield')
            data = db.session.query(User, Field.name).filter_by(usfield=usfield).join(Field, Field.id==User.usfield).all()
        else:
            data = db.session.query(User, Field.name).join(Field, Field.id==User.usfield).all()
        d = []
        for user, g_m in data:
            usr = user.format()
            usr["usfield"] = g_m
            d.append(usr)
        return jsonify(d)





@app.route("/api/user/<int:id>", methods=["GET", "POST"])
def userid(id):
    Usr = User.query.get_or_404(id)
    if request.method == "GET":
        return jsonify(Usr.format())
    else:
        try:
            data = request.form
            Usr.name = data["name"]
            Usr.email = data["email"]
            Usr.login = data["login"]
            Usr.password = data["password"]
            Usr.google_in = data["google_in"]
            Usr.org_id = data["org_id"]
            Usr.scolar_degree = data["scolar_degree"]
            Usr.user_lvl = data["user_lvl"]
            Usr.phone = data["phone"]
            Usr.usfield = data["usfield"]
            db.session.commit()
        except Exception as E:
            return jsonify({"msg": str(E)}), 400
        return jsonify({"msg" : "Succes"}), 200

@app.route("/api/user/delete/<int:id>", methods=["GET"])
def del_user(id):
    Usr = User.query.get_or_404(id)
    try:
        db.session.delete(Usr)
        db.session.commit()
    except Exception as E:
        return jsonify({"msg" : str(E)}), 400
    return jsonify({"msg" : "Success"}), 200


def Send_EMAIL(email, txt, title):
    try:
        msg = Message(title,recipients=[email])
        msg.sender=("Al-Khorezmiy", "no-reply@ladymarykay.uz")
        msg.html = '<h3>%s</h3>'%txt
        mail.send(msg)
    except Exception as E:
        return False, str(E)
    return True, True

@app.route('/api/email', methods=['GET', 'POST'])
def send_email():
    print('1sendemail')
    email = request.args.get('email')

    st, msg = Send_EMAIL(email, 'Hello')

    if st:
        return jsonify({"Success" : True})
    else:
        return jsonify(msg)
    

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

@app.route('/confirm/<string:token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash('Account already confirmed. Please login.', 'warning')
        else:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            flash('You have confirmed your account. Thanks!', 'success')
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
    return redirect(url_for('index'))

# @user_registered.connect_via(app)     
# def user_registered_sighandler(app, user, confirm_token):               
#     default_role = user_datastore.find_role("user")         
#     user_datastore.add_role_to_user(user, default_role)            
#     db.session.commit()
