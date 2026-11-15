from decimal import Decimal

from app.models import Transaction, User


def test_add_expense_saves_for_current_user(app, logged_in_client):
    data = {"amount": "12.50", "category": "Food", "date": "2026-11-01", "description": "Groceries"}
    response = logged_in_client.post("/transactions/new", data=data)
    assert response.status_code == 302

    with app.app_context():
        user = User.query.filter_by(username="alice").first()
        expense = Transaction.query.one()
        assert expense.user_id == user.id
        assert expense.type == "expense"
        assert expense.amount == Decimal("12.50")


def test_add_expense_rejects_invalid_amount(app, logged_in_client):
    data = {"amount": "0", "category": "Food", "date": "2026-11-01"}
    response = logged_in_client.post("/transactions/new", data=data)
    assert response.status_code == 400

    with app.app_context():
        assert Transaction.query.count() == 0
