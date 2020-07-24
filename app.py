from collections import OrderedDict
import os
import re
from services.services import ProductService


def is_integer(var):
    return re.search(r'^\d+$', var)


# Code from Treehouse Course https://teamtreehouse.com/library/using-databases-in-python/gettin-crudy-with-it/clean-up
def menu_loop():
    """Show the menu"""
    choice = None
    err = False

    while choice != 'q':
        clear()
        if err:
            print(err)
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()
        clear()

        if choice in menu:
            err = False
            clear()
            menu[choice]()
        else:
            err = f"{choice} is an invalid Option, Please try Again"


def clear():
    if os.environ.get('DEBUG', False) != 'true':
        os.system('cls' if os.name == 'nt' else 'clear')


def view_product():
    """View a single product's inventory"""
    print("Enter 'q' to quit.")
    user_input = None
    while user_input != 'q':
        user_input = input('Please enter valid Product ID: ').strip()
        clear()
        print("Enter 'q' to quit.")
        if user_input == 'q':
            break

        product, err, err_msg = ProductService.get_product_by_id(user_input)
        if err:
            clear()
            print("Enter 'q' to quit.")
            print(err_msg)
            continue

        print(f"""
    Name: {product['product_name']}
    Quantity: {product['product_quantity']}
    Price: {ProductService.get_product_price(product['product_price'])}
    Last Updated: {product['date_updated']}
    """)


def add_product():
    """Add a new product to the database"""
    clear()
    product_data = dict({
        'product_name': '',
        'product_quantity': '',
        'product_price': '',
    })
    for entry in product_data.keys():
        key_list = [k.capitalize() for k in entry.split('_')]
        err = False
        while True:
            if err:
                print(err)

            product_data[entry] = input(f"Please enter {' '.join(key_list)}: ").strip()
            if entry == 'product_price':
                # Inspired by https://stackoverflow.com/questions/354044/what-is-the-best-u-s-currency-regex
                # https://regex101.com/r/nekDuB/2
                price = re.search(r'^\$?[+-]?(?P<dollars>[0-9]{1,3}(?:,?[0-9]{3})*)(?:\.(?P<cents>[0-9]{2}))?$',
                                  product_data[entry])
                if not price:
                    err = f'Please enter a valid price amount'
                    continue
                price_dict = price.groupdict()
                if not price_dict['dollars']:
                    err = f'Please Enter valid Dollars amount'
                    continue

                price_dict['dollars'] = price_dict['dollars'].replace(',', '')
                if not is_integer(price_dict['dollars']):
                    err = f'Entered invalid dollars amount, Please try again..'
                    continue

                if not price_dict['cents']:
                    price_dict['cents'] = ''

                product_data[entry] = price_dict['dollars'] + price_dict['cents']

            elif entry == 'product_name':
                if not product_data[entry]:
                    err = f'{product_data[entry]} is not a Valid Product Name, Please try again...'
                    continue

            else:
                if not is_integer(product_data[entry]):
                    err = f'{product_data[entry]} is not a Valid Quantity, Please Try again... '
                    continue
            break

    if input('Save entry? [Yn] ').lower() != 'n':
        ProductService.create_record(product_data)


def backup_inventory():
    """Make a backup of the entire inventory"""
    ProductService.backup_database(db_format='csv', filepath='storage/backup.csv')
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
