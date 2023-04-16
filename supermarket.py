from datetime import datetime
from product import Product


class SuperMarket:
    def __init__(self, name, code, address):
        self.name = name
        self.code = code
        self.address = address
        self.date = datetime.now().replace(microsecond=0)
        self.products = []

    def add_item(self, item, quantity):
        """append an item after adding from the user"""
        item.quantity = item.quantity - quantity
        item_to_add = Product(item.item_code,
                              item.item_name,
                              item.item_exp_date,
                              item.purchasing_cost,
                              item.sell_cost,
                              quantity
                              )
        self.products.append(item_to_add)

    def read_item(self, item):
        """append an item that has been read from a file"""
        self.products.append(item)

    def write_items(self):
        """write the object items to a file"""
        file = open("DistributedItems_"+self.code+".txt", "w")
        for item in self.products:
            file.write(item.item_code + ";" +
                       item.item_name + ";" +
                       str(datetime.strftime(item.item_exp_date, "%d/%m/%Y")) + ";" +
                       str(item.purchasing_cost) + ";" +
                       str(item.sell_cost) + ";" +
                       str(item.quantity) + "\n"
                       )
