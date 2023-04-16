from datetime import datetime
from management_system import ManagementSystem


def main():
    """Main program starts here"""
    managementSystem = ManagementSystem()
    managementSystem.read_items("warehouse_items.txt")
    managementSystem.read_markets("warehouse_markets.txt")
    managementSystem.read_all_distributions()

    option = -1

    while option != 7:
        """Menu"""
        print("Please choose an option:")
        print("1. Add product items to the warehouse;")
        print("2. Add a new supermarket to the management system;")
        print("3. List of items in the warehouse based on expiry date;")
        print("4. Clear an item from the warehouse;")
        print("5. Distribute products from the warehouse to a supermarket;")
        print("6. Generate a report about the sales status of the warehouse;")
        print("7. Exit;")

        option = str(input())

        if option == '1':
            add_item(managementSystem)
            managementSystem.write_items("warehouse_items.txt")
            managementSystem.write_markets("warehouse_markets.txt")
            managementSystem.write_markets_items()
        elif option == '2':
            add_supermarket(managementSystem)
            managementSystem.write_items("warehouse_items.txt")
            managementSystem.write_markets("warehouse_markets.txt")
            managementSystem.write_markets_items()
        elif option == '3':
            list_items(managementSystem)
            managementSystem.write_items("warehouse_items.txt")
            managementSystem.write_markets("warehouse_markets.txt")
            managementSystem.write_markets_items()
        elif option == '4':
            clear_item(managementSystem)
            managementSystem.write_items("warehouse_items.txt")
            managementSystem.write_markets("warehouse_markets.txt")
            managementSystem.write_markets_items()
        elif option == '5':
            distribute_product(managementSystem)
            managementSystem.write_items("warehouse_items.txt")
            managementSystem.write_markets("warehouse_markets.txt")
            managementSystem.write_markets_items()
        elif option == '6':
            report(managementSystem)
        elif option == '7':
            print("Thank you for using the management system app")
            exit(1)
        else:
            print("Please choose a valid option")


def fourDigits(string):
    """check if the string is 4 digits"""
    try:
        int(string)
        if len(string) == 4:
            return True
        else:
            return False
    except:
        return False


def checkDate(date):
    """check if the date is valid"""
    try:
        datetime.strptime(date, '%d/%m/%Y')
        return True
    except:
        return False


def checkFloat(string):
    """check if the string is a float"""
    try:
        float(string)
        return True
    except:
        return False


def add_item(managementSystem: ManagementSystem):
    """read item attributes and add the object to the system"""
    code = str(input("Item code: "))
    while True:
        if not fourDigits(code):
            code = str(
                input("Item code must be 4 digits only ==> Enter again: "))
        elif fourDigits(code) and managementSystem.search_for_item(code):
            option = str(input(
                "\nItem already exists ==> Do you want to add a new quantity? (y/Y) for yes: "))
            if (option == 'y' or option == 'Y'):
                quantity_to_add = int(input("Enter the new quantity: "))
                code, old_name, old_exp_date, old_purchasing_cost, old_sell_cost = managementSystem.get_item_info(
                    code)
                old_exp_date = datetime.strptime(old_exp_date, '%d/%m/%Y')
                managementSystem.add_item(code, old_name, old_exp_date, float(
                    old_purchasing_cost), float(old_sell_cost), int(quantity_to_add))
                return
            code = str(input("Item already exists == > Enter again: "))
        else:
            break

    name = str(input("Item name: "))
    date = str(input("Expiry date (DD/MM/YYYY): "))
    while not checkDate(date):
        date = str(input("Invalid date ==> Enter again: "))
    expiry_date = datetime.strptime(date, '%d/%m/%Y')
    unit_cost = input("Wholesale unit cost: ")
    while not checkFloat(unit_cost):
        unit_cost = input("Invalid unit cost ==> Enter again: ")
    sell_cost = input("Sell cost: ")
    while not checkFloat(sell_cost):
        sell_cost = input("Invalid sell cost ==> Enter again: ")
    quantity = input("Quantity: ")
    while not quantity.isnumeric():
        quantity = input("Invalid quantity ==> Enter again: ")
    managementSystem.add_item(code, name, expiry_date, float(
        unit_cost), float(sell_cost), int(quantity))


def add_supermarket(managementSystem: ManagementSystem):
    """read market attributes and add the object to the system"""
    name = str(input("SuperMarket name: "))
    code = str(input("SuperMarket code: "))
    while True:
        if managementSystem.search_for_supermarket(code):
            code = str(input("Supermarket already exists == > Enter again: "))
        else:
            break
    address = str(input("SuperMarket address: "))
    managementSystem.add_supermarket(name, code, address)


def list_items(managementSystem: ManagementSystem):
    """read the date and get the items from the system"""
    try:
        datestr = input("Enter a specific date (DD/MM/YYYY): ")
        date = datetime.strptime(datestr, '%d/%m/%Y')
        managementSystem.list_items(date)
    except Exception as e:
        print(str(e))


def clear_item(managementSystem: ManagementSystem):
    """reading the item code and quantity to remove it by the system"""
    code = str(input("Item code: "))
    while True:
        if not fourDigits(code):
            code = str(
                input("Item code must be 4 digits only ==> Enter again: "))
        else:
            break
    
    if managementSystem.search_for_item(code):
        quantity = int(input("Enter quantity: "))
        managementSystem.remove_from_items(code, quantity)
    else:
        print("Item does not exist\n")


def distribute_product(managementSystem: ManagementSystem):
    """distribute a product to a supermarket"""
    option = 'y'
    market_code = str(input("\nSuperMarket code: "))
    if managementSystem.search_for_supermarket(market_code):
        while option == 'y' or option == 'Y':
            item_code = str(input("Item code: "))
            if managementSystem.search_for_item(item_code):
                quantity = int(input("Quantity: "))
                if quantity < 1:
                    print("Invalid input\n")
                    break
                if managementSystem.available_item(item_code) >= quantity:
                    print("Needed quantity is sent now")
                    managementSystem.send_to_supermarket(
                        item_code, market_code, quantity)
                elif managementSystem.available_item(item_code) > 0:
                    print("Available quantity is: " +
                          str(managementSystem.available_item(item_code)))
                    print("The not sent quantity is: " + str(quantity -
                          managementSystem.available_item(item_code)))
                    print("Sending ...")
                    managementSystem.send_to_supermarket(
                        item_code, market_code, managementSystem.available_item(item_code))
                else:
                    print("This item is not available right now...")
            else:
                quantity = int(input("Quantity: "))
                if not fourDigits(item_code):
                    print("Item code must be 4 digits only")
                else:
                    print("***********\nItem does not exist")
                print("The code of the item is: " + str(item_code) + " and the requested amount is: " + str(quantity))
            option = str(
                input("\nDo you want to send another item? y/Y for yes or type anything to exit: "))
            item_code = ''
            quantity = 0
    else:
        print("this supermarket does not exist")


def report(managementSystem: ManagementSystem):
    """get items report from the system"""
    managementSystem.generate_report()


if __name__ == "__main__":
    main()
