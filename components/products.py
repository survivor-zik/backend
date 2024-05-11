import pymongo
from pymongo import MongoClient

MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "your_database_name"
PRODUCTS_COLLECTION = "products"
PURCHASES_COLLECTION = "purchases"


def get_database():
    client = MongoClient(MONGODB_URI)
    return client[DATABASE_NAME]


def get_products_collection():
    """Gets or creates the 'products' collection."""
    db = get_database()
    return db[PRODUCTS_COLLECTION]




# Example usage
products_collection = get_products_collection()
