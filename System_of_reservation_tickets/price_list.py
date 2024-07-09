class PriceList:
    prices = {
        "normal": 20.00,
        "student": 16.00,
        "pensioner": 14.00,
        "child_under_10": 10.00
    }

    def add_special_discount(self, discount_name: str, discount_price: float):
        if discount_name not in self.prices:
            self.prices.update({discount_name: discount_price})
        print(self.prices)

    def delete_special_discount(self, discount_name: str):
        if discount_name in self.prices:
            self.prices.pop(discount_name)
        print(self.prices)

    def change_price(self, discount_name: str, discount_price: float):
        if discount_name in self.prices:
            self.prices[discount_name] = discount_price
        print(self.prices)

    def calculate_discount_percentage(self, discount_name: str):
        if discount_name in self.prices:
            new_price_percentage = 100 * self.prices[discount_name] / self.prices["normal"]
            return str(100 - int(new_price_percentage)) + "%"

    def get_prices(self):
        return self.prices
