from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>SpendSmart</h1><p>Personal Spending Tracker</p>"


if __name__ == "__main__":
    app.run(debug=True)