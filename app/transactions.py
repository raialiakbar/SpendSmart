from datetime import date
from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.auth import login_required
from app.extensions import db
from app.models import CATEGORIES, PAYMENT_METHODS, Transaction

transactions = Blueprint("transactions", __name__, url_prefix="/transactions")


def parse_transaction_form(form):
    errors = []
    data = {}

    raw_amount = form.get("amount", "").strip().replace(",", ".")
    try:
        amount = Decimal(raw_amount)
        if not amount.is_finite() or amount <= 0:
            errors.append("Amount must be greater than 0.")
        elif amount.as_tuple().exponent < -2:
            errors.append("Amount can have at most 2 decimal places.")
        elif amount >= Decimal("100000000"):
            errors.append("Amount is too large.")
        else:
            data["amount"] = amount
    except InvalidOperation:
        errors.append("Please enter a valid amount.")

    category = form.get("category", "").strip()
    if category not in CATEGORIES:
        errors.append("Please choose a category.")
    else:
        data["category"] = category

    raw_date = form.get("date", "").strip()
    if not raw_date:
        data["date"] = date.today()
    else:
        try:
            data["date"] = date.fromisoformat(raw_date)
        except ValueError:
            errors.append("Please enter a valid date.")

    description = form.get("description", "").strip()
    if len(description) > 255:
        errors.append("Description can be at most 255 characters.")
    else:
        data["description"] = description or None

    payment_method = form.get("payment_method", "").strip()
    if payment_method and payment_method not in PAYMENT_METHODS:
        errors.append("Please choose a valid payment method.")
    else:
        data["payment_method"] = payment_method or None

    return data, errors


@transactions.route("/")
@login_required
def list_transactions():
    return render_template("transactions.html")


@transactions.route("/new", methods=["GET", "POST"])
@login_required
def add_expense():
    if request.method == "POST":
        data, errors = parse_transaction_form(request.form)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "transaction_form.html",
                form=request.form,
                categories=CATEGORIES,
                payment_methods=PAYMENT_METHODS,
            ), 400

        expense = Transaction(type="expense", user_id=session["user_id"], **data)
        db.session.add(expense)
        db.session.commit()

        flash("Expense added.", "success")
        return redirect(url_for("transactions.list_transactions"))

    return render_template(
        "transaction_form.html",
        form={"date": date.today().isoformat()},
        categories=CATEGORIES,
        payment_methods=PAYMENT_METHODS,
    )
