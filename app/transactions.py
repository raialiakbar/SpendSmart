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
from app.models import CATEGORIES, PAYMENT_METHODS, TRANSACTION_TYPES, Transaction

transactions = Blueprint("transactions", __name__, url_prefix="/transactions")


def parse_transaction_form(form):
    errors = []
    data = {}

    transaction_type = form.get("type", "expense")
    if transaction_type not in TRANSACTION_TYPES:
        errors.append("Please choose expense or income.")
    else:
        data["type"] = transaction_type

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
    user_transactions = (
        Transaction.query.filter_by(user_id=session["user_id"])
        .order_by(Transaction.date.desc(), Transaction.id.desc())
        .all()
    )
    return render_template(
        "transactions.html",
        transactions=user_transactions,
        transaction_types=TRANSACTION_TYPES,
    )


def render_form(form, title, status=200):
    return render_template(
        "transaction_form.html",
        form=form,
        title=title,
        categories=CATEGORIES,
        payment_methods=PAYMENT_METHODS,
        transaction_types=TRANSACTION_TYPES,
    ), status


@transactions.route("/new", methods=["GET", "POST"])
@login_required
def add_transaction():
    if request.method == "POST":
        data, errors = parse_transaction_form(request.form)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_form(request.form, "Add transaction", 400)

        transaction = Transaction(user_id=session["user_id"], **data)
        db.session.add(transaction)
        db.session.commit()

        flash(f"{TRANSACTION_TYPES[transaction.type]} added.", "success")
        return redirect(url_for("transactions.list_transactions"))

    transaction_type = request.args.get("type", "expense")
    if transaction_type not in TRANSACTION_TYPES:
        transaction_type = "expense"
    form = {"type": transaction_type, "date": date.today().isoformat()}
    return render_form(form, f"Add {transaction_type}")
