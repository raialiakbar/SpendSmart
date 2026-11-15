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


def test_add_income_saves_for_current_user(app, logged_in_client):
    data = {"type": "income", "amount": "1500", "category": "Salary", "date": "2026-11-01"}
    response = logged_in_client.post("/transactions/new", data=data)
    assert response.status_code == 302

    with app.app_context():
        income = Transaction.query.one()
        assert income.type == "income"
        assert income.amount == Decimal("1500.00")


def test_transactions_list_shows_details(app, logged_in_client):
    data = {"amount": "12.50", "category": "Food", "date": "2026-11-01", "description": "Groceries"}
    logged_in_client.post("/transactions/new", data=data)

    response = logged_in_client.get("/transactions/")
    assert response.status_code == 200
    for text in [b"01.11.2026", b"Expense", b"Food", b"12.50", b"Groceries"]:
        assert text in response.data
