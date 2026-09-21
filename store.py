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
        """Purchase each shopping list entry and return the total price."""
        total_price = 0.0

        for product, quantity in shopping_list:
            if product not in self.products:
                raise ValueError("Product is not available in this store.")

            total_price += product.buy(quantity)

        return total_price


def main():
    """Run a demonstration of the Store class."""
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
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
