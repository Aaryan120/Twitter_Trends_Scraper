from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from app.config import Config

MONGODB_URL = Config.DB_CONNECTION_STRING
DB_NAME = Config.DB_NAME
COLLECTION_NAME = Config.COLLECTION_NAME


client = MongoClient(MONGODB_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def get_all_records(object_id):
    try:
        global client,db,collection

        if not client.is_primary:
            client = MongoClient(MONGODB_URL)

        record = (collection.find_one({"_id": ObjectId(object_id)}))

        if record:
            record["_id"] = str(record["_id"])  # Convert ObjectId to string
            return record
        else:
            return []
    except Exception as e:
        print(f'Error retrieving records: {e}')
        return []


def save_trend(trends,ip_address):
    try:
        global client,db,collection

        if not client.is_primary:
            client = MongoClient(MONGODB_URL)

        document = {
            "trends":trends,
            "timestamp": datetime.now(),
            "ip_address":ip_address
        }

        result = collection.insert_one(document)
        return result.inserted_id
    except Exception as e:
        print(f'Could not save the entry: {e}')
        return None

