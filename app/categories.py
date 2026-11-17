"""Predefined transaction categories (US-26).

This is the single place that defines which categories exist. Other code
(add/edit forms, transaction list, dashboard) should import from here
instead of typing the names again.

    from app.categories import CATEGORIES
"""

CATEGORIES = [
    "Rent",
    "Food",
    "Transport",
    "Shopping",
    "Salary",
    "Other",
]


def is_valid_category(name):
    """Return True if `name` is one of the predefined categories."""
    return name in CATEGORIES