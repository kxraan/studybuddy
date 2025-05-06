# inspect_db.py
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, serverSelectionTimeoutMS=5000)

# get default database from URI
db = client.get_database()
print("▶ Default database name:", db.name)
print("▶ Collections:", db.list_collection_names())

# show last 5 users
print("▶ Last 5 users:")
for u in db.users.find().sort('_id', -1).limit(5):
    print(f"  • {u.get('username')} <{u.get('email')}>")
