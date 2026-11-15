from decimal import Decimal

from app.models import Transaction, User
from tests.conftest import create_user, login


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


def test_user_only_sees_own_transactions(app, client):
    create_user(app, "alice", "alice@example.com")
    create_user(app, "bob", "bob@example.com")

    login(client, "alice")
    data = {"amount": "99", "category": "Rent", "date": "2026-11-01", "description": "Alice rent"}
    client.post("/transactions/new", data=data)
    client.post("/logout")

    login(client, "bob")
    response = client.get("/transactions/")
    assert b"Alice rent" not in response.data
    assert b"No transactions yet" in response.data


def test_edit_transaction_saves_changes(app, logged_in_client):
    data = {"amount": "12.50", "category": "Food", "date": "2026-11-01", "description": "Groceries"}
    logged_in_client.post("/transactions/new", data=data)

    with app.app_context():
        transaction_id = Transaction.query.one().id

    data.update(amount="20", description="Dinner")
    response = logged_in_client.post(f"/transactions/{transaction_id}/edit", data=data)
    assert response.status_code == 302

    with app.app_context():
        transaction = Transaction.query.one()
        assert transaction.amount == Decimal("20.00")
        assert transaction.description == "Dinner"


def test_delete_transaction(app, logged_in_client):
    data = {"amount": "12.50", "category": "Food", "date": "2026-11-01"}
    logged_in_client.post("/transactions/new", data=data)

    with app.app_context():
        transaction_id = Transaction.query.one().id

    response = logged_in_client.post(
        f"/transactions/{transaction_id}/delete", follow_redirects=True
    )
    assert b"Transaction deleted." in response.data

    with app.app_context():
        assert Transaction.query.count() == 0
