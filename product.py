from datetime import datetime
from decimal import InvalidOperation


class Product:
    def __init__(self, item_code: str, item_name, item_exp_date, purchasing_cost, sell_cost, quantity):
        """Constructor"""
        if item_exp_date < datetime.now():
            raise InvalidOperation("We can't add an expired product")
        self.item_code = item_code
        self.item_name = item_name
        self.item_exp_date = item_exp_date
        self.purchasing_cost = purchasing_cost
        self.sell_cost = sell_cost
        self.quantity = quantity

    def equals(self, item):
        """Returns true if the item is equal to the current item"""
        if self.item_code == item.item_code and self.item_name == item.item_name and self.item_exp_date == item.item_exp_date and self.purchasing_cost == item.purchasing_cost and self.sell_cost == item.sell_cost:
            return True
        return False
