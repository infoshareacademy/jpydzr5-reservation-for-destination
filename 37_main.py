class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        self.items.append({"product": product, "quantity": quantity})

    def display_cart(self):
        if not self.items:
            print("Koszyk jest pusty!")
        else:
            for item in self.items:
                product = item["product"]
                quantity = item["quantity"]
                print(f"{product} - Quantity: {quantity}")

    def remove_item(self, product):
        if not self.items:
            print("Koszyk jest pusty!")
            return
        for item in self.items:
            if item["product"] == product:
                self.items.remove(item)
                print(f"Removed {product}")
                return
            print(f"Product {product} not found in the cart.")