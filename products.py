class Product:
    """Represent a product with a price and stock quantity."""

    def __init__(self, name, price, quantity):
        """Initialize the product and validate its initial values."""
        if not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name
        self.price = float(price)
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> int:
        """Return the current stock quantity."""
        return self.quantity

    def set_quantity(self, quantity):
        """Update stock quantity and deactivate the product when empty."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity

        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Return whether the product is active."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def show(self):
        """Print the product details."""
        print(
            f"{self.name}, Price: {self.price:g}, "
            f"Quantity: {self.quantity}"
        )

    def buy(self, quantity) -> float:
        """Purchase the requested quantity and return its total price."""
        if not self.active:
            raise ValueError("Product is inactive.")
        if quantity <= 0:
            raise ValueError("Purchase quantity must be greater than zero.")
        if quantity > self.quantity:
            raise ValueError("Not enough stock.")

        total_price = self.price * quantity
        self.set_quantity(self.quantity - quantity)
        return total_price


def main():
    """Run a demonstration of the Product class."""
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.set_quantity(1000)
    bose.show()


if __name__ == "__main__":
    main()
