import pymongo
from pymongo import MongoClient

MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "your_database_name"
PRODUCTS_COLLECTION = "products"
PURCHASES_COLLECTION = "purchases"


def get_database():
    client = MongoClient(MONGODB_URI)
    yield client[DATABASE_NAME]


def get_purchases_collection():
    """Gets or creates the 'purchases' collection."""
    db = get_database()
    return db[PURCHASES_COLLECTION]


purchases_collection = get_purchases_collection()
