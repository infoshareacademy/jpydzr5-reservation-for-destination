class PriceList:
    prices = {
        "Normalny": 20.00,
        "Student": 16.00,
        "Emeryt": 14.00,
        "Dziecko do 10 lat": 10.00
    }
    prices_limit = 8

    def add_special_discount(self, discount_name: str, discount_price: float):
        if discount_name in self.prices:
            print(f"Zniżka {discount_name} już istnieje.")
        elif len(self.prices) >= self.prices_limit:
            print("Przekroczono ilość zniżek.")
        else:
            self.prices.update({discount_name: discount_price})

    def delete_special_discount(self, discount_name: str):
        if discount_name in self.prices:
            self.prices.pop(discount_name)
        else:
            print(f"Zniżka {discount_name} nie istnieje.")

    def change_price(self, discount_name: str, discount_price: float):
        if discount_name in self.prices:
            self.prices[discount_name] = discount_price
        else:
            print(f"Zniżka {discount_name} nie istnieje.")

    def calculate_discount_percentage(self, discount_name: str):
        if discount_name in self.prices:
            new_price_percentage = 100 * self.prices[discount_name] / self.prices["Normalny"]
            return str(100 - int(new_price_percentage)) + "%"
        else:
            print(f"Zniżka {discount_name} nie istnieje.")

    def get_prices(self):
        return self.prices

    def get_price_by_name(self, name):
        return self.prices[name]

    def __str__(self):
        header = "Cennik biletów:"
        body = "\n".join([f"{key}: {value:.2f} PLN" for key, value in self.prices.items()])
        return f"{header}\n{body}"
