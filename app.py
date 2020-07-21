from collections import OrderedDict
import os
from services.services import ProductService


# Code from Treehouse Course https://teamtreehouse.com/library/using-databases-in-python/gettin-crudy-with-it/clean-up
def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()
        clear()

        if choice in menu:
            clear()
            menu[choice]()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def view_product():
    """View a single product's inventory"""
    print("Enter 'q' to quit.")
    user_input = input('Please enter valid Product ID: ').strip()
    if user_input == 'q':
        return
    try:
        product = ProductService.get_product_by_id(user_input)
        print(f"""
Name: {product['product_name']}
Quantity: {product['product_quantity']}
Price: {ProductService.get_product_price(product['product_price'])}
Last Updated: {product['date_updated']}
""")
    except ValueError:
        print('Invalid response')
        view_product()


def add_product():
    """Add a new product to the database"""
    pass


def backup_inventory():
    """Make a backup of the entire inventory"""
    ProductService.backup_database(format='csv', filepath='storage/backup.csv')
    print("Inventory is now Backed up")


menu = OrderedDict([
    ('a', add_product),
    ('b', backup_inventory),
    ('v', view_product),
])


if __name__ == '__main__':
    ProductService.import_database_by_csv('inventory.csv')
    menu_loop()
    ProductService.close()