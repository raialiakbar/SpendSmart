from flask import Blueprint, render_template

from app.auth import login_required


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@main.route("/transactions")
@login_required
def transactions():
    return render_template("transactions.html")
