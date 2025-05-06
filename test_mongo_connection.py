# test_mongo_connection.py

import os
from pymongo import MongoClient, errors

def test_connection():
    uri = os.getenv('MONGO_URI')
    if not uri:
        print("❌  Environment variable MONGO_URI is not set.")
        return

    try:
        # Try to connect and ping the server
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅  MongoDB connection successful!")
    except errors.ServerSelectionTimeoutError as err:
        print(f"❌  Failed to connect to MongoDB: {err}")
    except Exception as exc:
        print(f"❌  An unexpected error occurred: {exc}")

if __name__ == '__main__':
    test_connection()
