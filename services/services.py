import csv
from models.product import Product
from playhouse.dataset import DataSet
from peewee import IntegrityError


class BaseService:
    model = None

    @classmethod
    def close(cls):
        cls.model.close()

    @classmethod
    def backup_database(cls, format, filepath):
        db = DataSet('sqlite:///:memory:')
        db.freeze(cls.model.select(), format=format, filename=filepath)


class ProductService(BaseService):
    model = Product
    Product.initialize()

    @classmethod
    def get_product_by_id(cls, product_id):
        try:
            return cls.model.select().where(cls.model.product_id == product_id).dicts().get(), False, None
        except cls.model.DoesNotExist:
            return None, True, f"The Queried value of {product_id} does not Exist, please try again"

    @classmethod
    def get_product_price(cls, price):
        return f"${str(price)[0:-2]}.{str(price)[-2:]}"

    @classmethod
    def create_record(cls, row):
        try:
            cls.model.create(**row)
        except IntegrityError as err:
            query = cls.model.select().where(cls.model.product_name == row['product_name'])
            if not len(query) == 1:
                raise IntegrityError(err)
            cls.model.update(**row).where(cls.model.product_name == row['product_name'])

    @classmethod
    def import_database_by_csv(cls, filepath):
        if not len(cls.model.select()) == 0:
            print("Database already contains data, Skipping csv initialization...")
            return

        print(f"Database Does not Exist, Seeding Database with {filepath}...")
        with open(filepath, newline='') as csvfile:
            products = csv.DictReader(csvfile, delimiter=',')
            for row in list(products):
                row['product_price'] = int(round(float(row['product_price'].strip('$')) * 100))
                cls.create_record(row)
