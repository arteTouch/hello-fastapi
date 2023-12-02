from pymongo import MongoClient


DB_URL = 'mongodb://localhost:27017'
DB_NAME = 'HELLO'

def get_db() -> MongoClient:
    try:
        client = MongoClient(DB_URL)
        db = client[DB_NAME]
        yield db
    finally:
        client.close()