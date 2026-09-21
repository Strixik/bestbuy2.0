import pytest

from products import Product, NonStockedProduct, LimitedProduct
from promotions import (
    Promotion,
    PercentDiscount,
    SecondHalfPrice,
    ThirdOneFree,
)
from store import Store


def test_promotion_base_class_is_abstract():
    with pytest.raises(TypeError):
        Promotion("Generic promotion")


def test_product_properties_and_string():
    product = Product("Mac", price=100, quantity=5)

    assert product.name == "Mac"
    assert product.price == 100
    assert product.quantity == 5
    assert "Mac" in str(product)
    assert "Price: $100" in str(product)

    product.quantity = 0
    assert not product.active


def test_negative_price_is_rejected():
    product = Product("Mac", price=100, quantity=5)

    with pytest.raises(ValueError):
        product.price = -100

    assert product.price == 100


def test_promotion_can_be_assigned_and_removed():
    product = Product("Mac", price=100, quantity=5)
    promotion = PercentDiscount("30% off", percent=30)

    product.promotion = promotion

    assert product.promotion is promotion
    assert "30% off" in str(product)
    assert product.buy(1) == pytest.approx(70)

    product.promotion = None

    assert product.promotion is None
    assert product.buy(1) == pytest.approx(100)


def test_product_price_comparison():
    mac = Product("Mac", price=100, quantity=5)
    bose = Product("Bose", price=50, quantity=5)

    assert mac > bose
    assert bose < mac
    assert not mac < bose


def test_store_contains_product():
    mac = Product("Mac", price=100, quantity=5)
    bose = Product("Bose", price=50, quantity=5)
    shop = Store([mac])

    assert mac in shop
    assert bose not in shop


def test_adding_stores_creates_a_new_store():
    mac = Product("Mac", price=100, quantity=5)
    bose = Product("Bose", price=50, quantity=5)
    first_store = Store([mac])
    second_store = Store([bose])

    combined = first_store + second_store

    assert combined is not first_store
    assert combined is not second_store
    assert mac in combined
    assert bose in combined
    assert bose not in first_store


def test_second_item_is_half_price_even_when_ordered_separately():
    mac = Product("Mac", price=100, quantity=5)
    mac.promotion = SecondHalfPrice("Second half price")
    shop = Store([mac])

    assert shop.order([(mac, 1), (mac, 1)]) == pytest.approx(150)
    assert mac.quantity == 3


def test_every_third_item_is_free():
    bose = Product("Bose", price=50, quantity=5)
    bose.promotion = ThirdOneFree("Third one free")

    assert bose.buy(3) == pytest.approx(100)
    assert bose.quantity == 2


def test_non_stocked_product_keeps_zero_quantity_with_discount():
    license_product = NonStockedProduct("License", price=100)
    license_product.promotion = PercentDiscount("30% off", percent=30)
    shop = Store([license_product])

    assert license_product.active
    assert "Non-stocked" in str(license_product)
    assert shop.order([(license_product, 2)]) == pytest.approx(140)
    assert license_product.quantity == 0
    assert license_product.active


def test_limited_product_cannot_be_added_twice_to_one_order():
    shipping = LimitedProduct(
        "Shipping", price=10, quantity=5, maximum=1
    )
    shop = Store([shipping])

    with pytest.raises(ValueError):
        shop.order([(shipping, 1), (shipping, 1)])

    assert shipping.quantity == 5