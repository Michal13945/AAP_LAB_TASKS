# -*- coding: utf-8 -*-
"""Testy pytest dla klasy Product -- uzupelnij!

Uruchomienie: pytest test_product_pytest.py -v
"""

import pytest
from product import Product

@pytest.fixture
def product():
    return Product("Laptop", 2999.99, 10)

def test_is_available(product):
    assert product.is_available() is True

def test_total_value(product):
    assert product.total_value() == 2999.99 * 10

@pytest.mark.parametrize("amount, expected_quantity", [
    (5, 15),
    (0, 10),
    (100, 110),
])

def test_add_stock_parametrized(product, amount, expected_quantity):
    product.add_stock(amount)
    assert product.quantity == expected_quantity

def test_remove_stock_too_much_raises(product):
    with pytest.raises(ValueError):
        product.remove_stock(999)


def test_add_stock_negative_raises(product):
    with pytest.raises(ValueError):
        product.add_stock(-4)

@pytest.mark.parametrize("percent, expected_price", [
    (0, 2999.99),
    (50, 1499.995),
    (100, 0.0),
])
def test_apply_discount(product, percent, expected_price):
    product.apply_discount(percent)
    assert product.price == expected_price


@pytest.mark.parametrize("invalid_percent", [-10, -1, 101, 150])
def test_apply_discount_invalid_values(product, invalid_percent):
    with pytest.raises(ValueError):
        product.apply_discount(invalid_percent)