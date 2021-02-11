from flask import *

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return "Al Khorezmiy"

if __name__ == "__main__":
    app.run()