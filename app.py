from flask import *

app = Flask(__name__)




@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

@app.route('/test')
def test():
    return "Works!"

if __name__ == "__main__":
    app.run(threaded=True, port=5000)