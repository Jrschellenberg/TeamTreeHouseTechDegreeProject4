import datetime
from peewee import *


db = SqliteDatabase('storage/products.db')


class Product(Model):
    product_id = IntegerField(primary_key=True, unique=True)
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateField(default=datetime.datetime.now, formats=['%m/%d/%Y'])

    @classmethod
    def initialize(cls):
        db.connect()
        db.create_tables([Product], safe=True)

    @classmethod
    def close(cls):
        db.close()

    class Meta:
        database = db


if __name__ == '__main__':
    Product.initialize()
    Product.close()
