from abc import ABC, abstractmethod


class Promotion(ABC):
    """Base class for product promotions."""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """Return the total price after applying the promotion."""


class PercentDiscount(Promotion):
    """Reduce the total price by a percentage."""

    def __init__(self, name, percent):
        super().__init__(name)

        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100.")

        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        return product.price * quantity * (1 - self.percent / 100)


class SecondHalfPrice(Promotion):
    """Make every second item half price."""

    def apply_promotion(self, product, quantity) -> float:
        full_price_items = quantity - quantity // 2
        half_price_items = quantity // 2

        return (
            full_price_items * product.price
            + half_price_items * product.price / 2
        )


class ThirdOneFree(Promotion):
    """Make every third item free."""

    def apply_promotion(self, product, quantity) -> float:
        paid_items = quantity - quantity // 3
        return paid_items * product.price