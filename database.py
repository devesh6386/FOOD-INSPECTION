# database.py
import os 
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing from .env file")

client = AsyncIOMotorClient(MONGO_URI)
db = client["labelguard_db"]  # Database object imported in main.py
users_collection = db["users"]
"""from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://dev-46:AdminPass123@creature3.eb9voxx.mongodb.net/?appName=Creature3"
client = AsyncIOMotorClient(MONGO_URI)

db = client.labelguard_db
users_collection = db.users
"""