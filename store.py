import products


class Store:
    """Manage a collection of products and process orders."""

    def __init__(self, product_list):
        """Initialize the store with a copy of the product list."""
        self.products = list(product_list)

    def add_product(self, product):
        """Add a product to the store."""
        self.products.append(product)

    def remove_product(self, product):
        """Remove a product from the store."""
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """Return the total number of items in stock."""
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self):
        """Return all active products."""
        return [
            product
            for product in self.products
            if product.is_active()
        ]

    def order(self, shopping_list) -> float:
        """Purchase products and return the total price."""
        requested = {}

        # Sum quantities when a product occurs multiple times.
        for product, quantity in shopping_list:
            if product not in self.products:
                raise ValueError("Product is not available in this store.")

            if quantity <= 0:
                raise ValueError(
                    "Purchase quantity must be greater than zero."
                )

            requested[product] = requested.get(product, 0) + quantity

        # Validate the entire order before purchasing any products.
        for product, quantity in requested.items():
            if not product.is_active():
                raise ValueError("Product is inactive.")

            if isinstance(product, products.LimitedProduct):
                if quantity > product.maximum:
                    raise ValueError(
                        f"Cannot buy more than "
                        f"{product.maximum} of this product."
                    )

            if not isinstance(product, products.NonStockedProduct):
                if quantity > product.get_quantity():
                    raise ValueError("Not enough stock.")

        total_price = 0.0

        # Buy each product once with its total quantity.
        for product, quantity in requested.items():
            total_price += product.buy(quantity)

        return total_price


def main():
    """Run a demonstration of the Store class."""
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product(
            "Bose QuietComfort Earbuds", price=250, quantity=500
        ),
        products.Product("Google Pixel 7", price=500, quantity=250),
    ]

    best_buy = Store(product_list)
    available_products = best_buy.get_all_products()

    print(best_buy.get_total_quantity())
    print(best_buy.order([
        (available_products[0], 1),
        (available_products[1], 2),
    ]))


if __name__ == "__main__":
    main()