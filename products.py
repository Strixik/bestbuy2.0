from promotions import Promotion


class Product:
    """Represent a product with a price and stock quantity."""

    def __init__(self, name, price, quantity):
        self._name = None
        self._price = None
        self._quantity = None
        self._active = True
        self._promotion = None

        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def name(self):
        """Return the product name."""
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Product name cannot be empty.")

        self._name = value

    @property
    def price(self):
        """Return the product price."""
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")

        self._price = float(value)

    @property
    def quantity(self):
        """Return the stock quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Quantity cannot be negative.")

        self._quantity = value

        if value == 0:
            self.deactivate()

    @property
    def active(self):
        """Return whether the product is active."""
        return self._active

    @property
    def promotion(self):
        """Return the current promotion."""
        return self._promotion

    @promotion.setter
    def promotion(self, value):
        if value is not None and not isinstance(value, Promotion):
            raise TypeError("Promotion must be a Promotion instance or None.")

        self._promotion = value

    def get_quantity(self) -> int:
        """Return the stock quantity."""
        return self.quantity

    def set_quantity(self, quantity):
        """Update the stock quantity."""
        self.quantity = quantity

    def is_active(self) -> bool:
        """Return whether the product is active."""
        return self.active

    def activate(self):
        """Activate the product."""
        self._active = True

    def deactivate(self):
        """Deactivate the product."""
        self._active = False

    def get_promotion(self):
        """Return the current promotion."""
        return self.promotion

    def set_promotion(self, promotion):
        """Assign or remove a promotion."""
        self.promotion = promotion

    def __str__(self):
        """Return a readable description of the product."""
        description = (
            f"{self.name}, Price: ${self.price:g}, "
            f"Quantity: {self.quantity}"
        )

        if self.promotion is not None:
            description += f", Promotion: {self.promotion.name}"

        return description

    def __gt__(self, other):
        """Compare product prices using >."""
        if not isinstance(other, Product):
            return NotImplemented

        return self.price > other.price

    def __lt__(self, other):
        """Compare product prices using <."""
        if not isinstance(other, Product):
            return NotImplemented

        return self.price < other.price

    def buy(self, quantity) -> float:
        """Purchase items and return the total price."""
        if not self.active:
            raise ValueError("Product is inactive.")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")
        if quantity > self.quantity:
            raise ValueError("Not enough stock.")

        total_price = (
            self.promotion.apply_promotion(self, quantity)
            if self.promotion is not None
            else self.price * quantity
        )

        self.quantity -= quantity
        return total_price


class NonStockedProduct(Product):
    """Represent a product without tracked stock."""

    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)
        self.activate()

    @Product.quantity.setter
    def quantity(self, value):
        """Keep the quantity at zero."""
        if value != 0:
            raise ValueError("A non-stocked product must have quantity 0.")

        self._quantity = 0

    def __str__(self):
        """Return a readable description of the product."""
        description = f"{self.name}, Price: ${self.price:g}, Non-stocked"

        if self.promotion is not None:
            description += f", Promotion: {self.promotion.name}"

        return description

    def buy(self, quantity) -> float:
        """Sell items without changing the stock quantity."""
        if not self.active:
            raise ValueError("Product is inactive.")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")

        if self.promotion is not None:
            return self.promotion.apply_promotion(self, quantity)

        return self.price * quantity


class LimitedProduct(Product):
    """Represent a product with a purchase limit per order."""

    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)

        if maximum <= 0:
            raise ValueError("Maximum must be greater than zero.")

        self.maximum = maximum

    def __str__(self):
        """Return a readable description of the product."""
        description = (
            f"{self.name}, Price: ${self.price:g}, "
            f"Quantity: {self.quantity}, Maximum: {self.maximum}"
        )

        if self.promotion is not None:
            description += f", Promotion: {self.promotion.name}"

        return description

    def buy(self, quantity) -> float:
        """Reject purchases above the limit."""
        if quantity > self.maximum:
            raise ValueError(
                f"Cannot buy more than {self.maximum} of this product."
            )

        return super().buy(quantity)