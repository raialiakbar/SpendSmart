from flask import Blueprint, render_template, session

from app.auth import login_required
from app.dashboard import get_summary
from app.extensions import db
from app.models import User


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    summary = get_summary(session["user_id"])
    user = db.session.get(User, session["user_id"])
    currency = user.currency if user else "EUR"
    return render_template("dashboard.html", summary=summary, currency=currency)


@main.route("/transactions")
@login_required
def transactions():
    return render_template("transactions.html")
