from app.categories import CATEGORIES, is_valid_category


def test_predefined_categories_are_available():
    assert CATEGORIES == ["Rent", "Food", "Transport", "Shopping", "Salary", "Other"]


def test_is_valid_category():
    assert is_valid_category("Food")
    assert not is_valid_category("Holidays")
    assert not is_valid_category("")