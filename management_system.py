from decimal import InvalidOperation
from product import Product
from supermarket import SuperMarket
from os.path import exists
from datetime import datetime


class ManagementSystem:
    def __init__(self, items: Product = [], SuperMarkets: SuperMarket = []):
        """constructor"""
        self.items = items
        self.SuperMarkets = SuperMarkets

    def read_items(self, filename):
        """read items from a file"""
        if exists(filename):
            with open(filename, "r") as fp:
                for line in fp.readlines():
                    info = line.split(";")
                    try:
                        """ info [0] = item_code, info [1] = item_name, info [2] = item_exp_date, info [3] = purchasing_cost, info [4] = sell_cost, info [5] = quantity"""
                        self.add_item(info[0], info[1], datetime.strptime(
                            info[2], "%d/%m/%Y"), float(info[3]), float(info[4]), int(info[5]))
                    except Exception as ex:
                        print(str(ex))

    def read_markets(self, filename):
        """read supermarkets from a file"""
        if exists(filename):
            with open(filename, "r") as fp:
                for line in fp.readlines():
                    info = line.split(";")
                    try:
                        """ info [0] = name, info [1] = code, info [2] = address"""
                        self.add_supermarket(
                            info[0], info[1], info[2].replace("\n", ""))
                    except Exception as ex:
                        print(str(ex))

    def write_markets(self, filename):
        """write markets to an output file"""
        outfile = open(filename, "w")
        for market in self.SuperMarkets:
            outfile.write(market.name + ";" +
                          market.code + ";" +
                          market.address + ";" +
                          str(market.date) + "\n"
                          )

    def write_markets_items(self):
        """to write items for each supermarket in the system to a new file"""
        for market in self.SuperMarkets:
            market.write_items()

    def read_all_distributions(self):
        """to read the markets' items"""
        for market in self.SuperMarkets:
            file = "DistributedItems_" + market.code + ".txt"
            if exists(file):
                """read items from a file"""
                with open(file, "r") as fp:
                    for line in fp.readlines():
                        try:
                            """add items to the supermarket"""
                            info = line.split(";")
                            """ info [0] = item_code, info [1] = item_name, info [2] = item_exp_date, info [3] = purchasing_cost, info [4] = sell_cost, info [5] = quantity"""
                            market.read_item(Product(info[0], info[1], datetime.strptime(
                                info[2], "%d/%m/%Y"), float(info[3]), float(info[4]), int(info[5])))
                            item_exists = False
                            for item in self.items:
                                if item.item_code == info[0]:
                                    item_exists = True
                                    break
                        except Exception as ex:
                            """print error message"""
                            print(str(ex))

    def write_items(self, filename):
        """write items to an output file"""
        outfile = open(filename, "w")
        for item in self.items:
            """write items to an output file"""
            outfile.write(item.item_code + ";" +
                          item.item_name + ";" +
                          str(datetime.strftime(item.item_exp_date, "%d/%m/%Y")) + ";" +
                          str(item.purchasing_cost) + ";" +
                          str(item.sell_cost) + ";" +
                          str(item.quantity) + "\n"
                          )

    def add_item(self, item_code, item_name, item_exp_date, unit_cost, sell_cost, quantity):
        """To add a new item to the system"""
        try:
            if quantity < 0:
                """check if the quantity is negative"""
                raise InvalidOperation("Quantity can't be less than 1")

            item = Product(item_code=item_code,
                           item_name=item_name,
                           item_exp_date=item_exp_date,
                           purchasing_cost=unit_cost,
                           sell_cost=sell_cost, quantity=quantity)

            for i in self.items:
                if i.equals(item):
                    i.quantity = i.quantity + quantity
                    print("quantity increased and the new quantity is: " + str(i.quantity))
                    return
                elif i.item_code == item.item_code:
                    raise InvalidOperation("Duplicate detected")

            self.items.append(item)
            print("Item " + str(item_code) + " is added")

        except BaseException as e:
            print(str(e))
            print("An error occurred, please see the explanation above")

    def add_supermarket(self, name, code, address):
        """adds a new supermarket to the system"""
        try:
            supermarket = SuperMarket(name, code, address)
            for market in self.SuperMarkets:
                if market.code == code:
                    raise InvalidOperation("Duplicate detected")

            self.SuperMarkets.append(supermarket)
            print("SuperMarket " + str(code) + " is added")
        except Exception as e:
            print(str(e))
            print("An error occurred, please see the expalnation above")

    def list_items(self, date):
        """list all the items that have an expiry date before an input date 'date'"""
        print("Items that have expiry date before the entered date:\n")
        totalcost = 0
        totalsell = 0
        for item in self.items:
            """check if the item is expired"""
            if item.item_exp_date < date:
                """print the item details"""
                print("item id: " + item.item_code + ", item name: " + item.item_name + ", expiry date:" + str(item.item_exp_date.date())
                      + ", item  cost: " + str(item.purchasing_cost) + ", sell cost:" + str(item.sell_cost) + ", quantity: " + str(item.quantity))
                """calculate the total cost and total sell"""
                totalcost = totalcost + (item.purchasing_cost * item.quantity)
                totalsell = totalsell + (item.sell_cost * item.quantity)

        if totalcost == 0 and totalsell == 0:
            print("No items found!\n")
        else:
            print("\n***********************")
            print("\nTotal wholesale cost of these items: " + str(totalcost))
            print("Total sales cost of these items: "+str(totalsell) + "\n")

    def search_for_item(self, code):
        """returns true if an item with code 'code' exists in the warehouse"""
        for item in self.items:
            if item.item_code == code:
                return True
        return False

    def available_item(self, code):
        """to return an item's quantity"""
        for item in self.items:
            if item.item_code == code:
                return item.quantity

    def get_item_info(self, code):
        """to return an item's details"""
        for item in self.items:
            if item.item_code == code:
                """ info [0] = item_code, info [1] = item_name, info [2] = item_exp_date, info [3] = purchasing_cost, info [4] = sell_cost, info [5] = quantity"""
                return item.item_code,item.item_name,datetime.strftime(item.item_exp_date, "%d/%m/%Y"),item.purchasing_cost,item.sell_cost


    def send_to_supermarket(self, item_code, market_code, quantity):
        """to send a product to a supermarket"""
        for item in self.items:
            if item.item_code == item_code:
                for market in self.SuperMarkets:
                    if market.code == market_code:
                        market.add_item(item, quantity)
                        if item.quantity == 0:
                            """remove the item from the warehouse"""
                            self.items.remove(item)
                        print("Sent items: " + str(quantity))
                        print("Done \n")
                        return

    def search_for_supermarket(self, code):
        """returns true if a supermarket with code 'code' exists in the warehouse"""
        for market in self.SuperMarkets:
            if market.code == code:
                return True
        return False

    def generate_report(self):
        """Generate report"""
        wholesale = 0
        sales = 0
        num_of_items = 0
        for item in self.items:
            if item.quantity > 0:
                """calculate the total wholesale cost of the items"""
                wholesale = wholesale + (item.purchasing_cost * item.quantity)
                sales = sales + (item.sell_cost * item.quantity)
                num_of_items = num_of_items + 1
        print("\nNumber of items in the warehouse = " + str(num_of_items))
        print("Total wholesale cost of all items in the warehouese: " + str(wholesale))
        print("Total sales cost of all items in the warehouse: " + str(sales))
        print("Expected profit after selling all items in the warehouse: " +
              str(sales - wholesale))
        print()

    def remove_from_items(self, code, quantity):
        """to remove items from the warehouse"""
        for item in self.items:
            if item.item_code == code:
                if item.quantity == quantity:
                    self.items.remove(item)
                    print("-- Success --\n")
                elif item.quantity > quantity:
                    item.quantity = item.quantity - quantity
                    print("-- Success --\n")
                elif item.quantity < quantity:
                    print(
                        "-- Operation Failed because the item quantity is less than the quantity entered -- \n")
