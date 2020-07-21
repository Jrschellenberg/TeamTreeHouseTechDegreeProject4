from services.services import ProductService

if __name__ == '__main__':
    ProductService.backup_database(format='csv', filepath='storage/backup.csv')
