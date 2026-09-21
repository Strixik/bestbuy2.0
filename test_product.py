import pytest

from products import Product


def test_create_product():
    product = Product("MacBook Air M2", price=1450, quantity=100)

    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.get_quantity() == 100
    assert product.is_active()


def test_invalid_product_details():
    with pytest.raises(Exception):
        Product("", price=1450, quantity=100)

    with pytest.raises(Exception):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_at_zero_quantity():
    product = Product("MacBook Air M2", price=1450, quantity=1)

    product.set_quantity(0)

    assert product.get_quantity() == 0
    assert not product.is_active()


def test_buy_changes_quantity_and_returns_total_price():
    product = Product("MacBook Air M2", price=1450, quantity=10)

    total_price = product.buy(2)

    assert product.get_quantity() == 8
    assert total_price == 2900


def test_buy_more_than_available_raises_exception():
    product = Product("MacBook Air M2", price=1450, quantity=3)

    with pytest.raises(Exception):
        product.buy(4)

    assert product.get_quantity() == 3