from playhouse.dataset import DataSet
from models.product import Product


class BaseService:
    model = None
    db = DataSet('sqlite:///:memory:')

    @classmethod
    def get_by_id(cls, id):
        return cls.model.select(id)

    @classmethod
    def backup_database(cls, format, filepath):
        cls.db.freeze(cls.model.select(), format=format, filename=filepath)


class ProductService(BaseService):
    model = Product

