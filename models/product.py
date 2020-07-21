from peewee import *


db = SqliteDatabase('storage/products.db')


class Product(Model):
    product_id = IntegerField(primary_key=True)

    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField()
    product_price = DecimalField(max_digits=8, decimal_places=2)
    date_updated = DateField(formats=['%m/%d/%Y'])

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    db.close()


