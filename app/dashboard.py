"""Dashboard calculations (US-28 to US-32).

All numbers shown on the dashboard are calculated here, for one user.
The route in routes.py only calls get_summary() and passes the result
to the template.
"""

from collections import defaultdict
from decimal import Decimal

from app.models import Transaction


def get_summary(user_id):
    """Return the dashboard numbers for the user with this id.

    Returns a dictionary with:
        total_income       (US-28) sum of all income
        total_expenses     (US-29) sum of all expenses
        balance            (US-30) total_income - total_expenses
        transaction_count  (US-31) number of transactions
        top_category       (US-32) name of the category with the highest
                                   expenses, or None if there are no expenses
        top_category_total (US-32) amount spent in that category
    """
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    total_income = Decimal("0")
    total_expenses = Decimal("0")
    expenses_by_category = {}
    expenses_by_month = defaultdict(Decimal)

    for transaction in transactions:
        if transaction.type == "income":
            total_income += transaction.amount
        elif transaction.type == "expense":
            total_expenses += transaction.amount
            expenses_by_category[transaction.category] = (
                expenses_by_category.get(transaction.category, Decimal("0"))
                + transaction.amount
            )
            month = transaction.date.strftime("%Y-%m")
            expenses_by_month[month] += transaction.amount

    top_category = None
    top_category_total = Decimal("0")
    if expenses_by_category:
        top_category = max(expenses_by_category, key=expenses_by_category.get)
        top_category_total = expenses_by_category[top_category]

    chart_data = {
        "income": float(total_income),
        "expenses": float(total_expenses)
    }
    category_chart_data = {
        "labels": list(expenses_by_category.keys()),
        "values": [float(amount) for amount in expenses_by_category.values()]
    }
    monthly_chart_data = {
        "labels": sorted(expenses_by_month.keys()),
        "values": [float(expenses_by_month[month]) for month in sorted(expenses_by_month.keys())]
    }

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": total_income - total_expenses,
        "transaction_count": len(transactions),
        "top_category": top_category,
        "top_category_total": top_category_total,
        "chart_data": chart_data,
        "category_chart_data": category_chart_data,
        "monthly_chart_data": monthly_chart_data,
    }