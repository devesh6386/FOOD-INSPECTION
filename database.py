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
