
from forms import *
from flask import jsonify, redirect
from flask_mail import Mail, Message





app.config["MAIL_SERVER"] = "server2.ahost.uz"
app.config["MAIL_PORT"] = 465
#app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USERNAME"] = 'odya@ladymarykay.uz'
app.config["MAIL_PASSWORD"] = 'Odilxon030101!'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@ladymarykay.uz'

mail = Mail(app)

# @app.route("/api/gettoken", methods=["GET"])
# def gettoken():
#     return GetToken()
@app.route("/api", methods=["GET"])
def main_api():
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
        )
        try:
            db.session.add(Usr)
            db.session.commit()
        except Exception as E:
            return jsonify({"msg" : str(E)}), 400
        return jsonify({"msg" : "Success"}), 200
    else:
        if request.args.get('og_id') is not None:
            og_id = request.args.get('org_id')
            data = db.session.query(User, Organisation.name).filter_by(org_id=og_id).join(Organisation, Organisation.id==User.org_id).all()
        else:
            data = db.session.query(User, Organisation.name).join(Organisation, Organisation.id==User.org_id).all()
        d = []
        for user, g_n in data:
            usr = user.format()
            usr["org_name"] = g_n
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


def Send_EMAIL(email, txt):
    try:
        msg = Message('Test',recipients=[email])
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
    
