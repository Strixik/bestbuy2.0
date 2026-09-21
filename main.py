import products
import store
import promotions


def show_products(product_list):
    """Print a numbered list of products."""
    print("------")

    for number, product in enumerate(product_list, start=1):
        print(f"{number}. ", end="")
        product.show()

    print("------")


def make_order(shop):
    """Collect an order from the user and process it."""
    available_products = shop.get_all_products()

    if not available_products:
        print("No active products available.")
        return

    show_products(available_products)
    shopping_list = []

    print("When you want to finish order, enter empty text.")

    while True:
        product_input = input("Which product # do you want? ").strip()

        if product_input == "":
            break

        try:
            product_number = int(product_input)

            if not 1 <= product_number <= len(available_products):
                raise ValueError("Invalid product number.")

            quantity = int(input("What amount do you want? "))

            if quantity <= 0:
                raise ValueError(
                    "Purchase quantity must be greater than zero."
                )

            product = available_products[product_number - 1]

            # Count quantities already added for this product.
            already_ordered = sum(
                amount
                for item, amount in shopping_list
                if item is product
            )

            requested_total = already_ordered + quantity

            if (
                    isinstance(product, products.LimitedProduct)
                    and requested_total > product.maximum
            ):
                raise ValueError(
                    f"Cannot buy more than {product.maximum} of this product."
                )

            if (
                    not isinstance(product, products.NonStockedProduct)
                    and requested_total > product.get_quantity()
            ):
                raise ValueError("Not enough stock.")

            shopping_list.append((product, quantity))
            print("Product added to list!\n")

        except ValueError as error:
            print(f"Error adding product: {error}\n")

    if not shopping_list:
        print("No products ordered.")
        return

    try:
        total_price = shop.order(shopping_list)
        print(f"Order completed! Total payment: ${total_price:.2f}")
    except ValueError as error:
        print(f"Order failed: {error}")


def start(shop):
    """Display the store menu and handle user choices."""
    while True:
        print("\n   Store Menu")
        print("   ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose a number: ").strip()

        if choice == "1":
            show_products(shop.get_all_products())
        elif choice == "2":
            print(f"Total of {shop.get_total_quantity()} items in store.")
        elif choice == "3":
            make_order(shop)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 4.")


def main():
    """Create the initial inventory and start the store interface."""
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product(
            "Bose QuietComfort Earbuds", price=250, quantity=500
        ),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct(
            "Shipping", price=10, quantity=250, maximum=1
        ),
    ]

    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
