import os
from pymongo import MongoClient

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")

client = MongoClient(DATABASE_URL)

db = client["erates"]

def get_collection(collection_name: str):
    def collection_generator():
        yield db[collection_name]
    return collection_generator
