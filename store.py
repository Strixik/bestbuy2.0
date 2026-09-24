import products


class Store:
    """Manage products and process orders."""

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
        """Return the total quantity of all active products."""
        return sum(
            product.quantity
            for product in self.products
            if product.active
        )

    def get_all_products(self):
        """Return all active products."""
        return [
            product
            for product in self.products
            if product.active
        ]

    def __contains__(self, product):
        """Return whether the store contains the product."""
        return product in self.products

    def __add__(self, other):
        """Combine two stores into a new store."""
        if not isinstance(other, Store):
            return NotImplemented

        return Store(self.products + other.products)

    def order(self, shopping_list) -> float:
        """Validate and purchase products."""
        requested = {}

        for product, quantity in shopping_list:
            if product not in self:
                raise ValueError("Product is not available in this store.")

            if quantity <= 0:
                raise ValueError(
                    "Purchase quantity must be greater than zero."
                )

            requested[product] = requested.get(product, 0) + quantity

        for product, quantity in requested.items():
            if not product.active:
                raise ValueError("Product is inactive.")

            if isinstance(product, products.LimitedProduct):
                if quantity > product.maximum:
                    raise ValueError(
                        f"Cannot buy more than "
                        f"{product.maximum} of this product."
                    )

            if not isinstance(product, products.NonStockedProduct):
                if quantity > product.quantity:
                    raise ValueError("Not enough stock.")

        total_price = 0.0

        for product, quantity in requested.items():
            total_price += product.buy(quantity)

        return total_price