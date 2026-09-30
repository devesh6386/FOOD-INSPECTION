import asyncio
from database import users_collection
from security import get_password_hash

async def seed_atlas():
    # Clear existing users to prevent duplicates
    await users_collection.delete_many({})

    users_to_add = [
        {
            "employee_id": "ADM-9002",
            "hashed_password": get_password_hash("adminpass123"),
            "role": "Admin",
            "full_name": "Senior Administrator H. S. Mathur",
            "jurisdiction": "Central Headquarters"
        },
        {
            "employee_id": "ADM-4455",
            "hashed_password": get_password_hash("adminpass456"),
            "role": "Admin",
            "full_name": "Director of Enforcement",
            "jurisdiction": "Regional Headquarters"
        },
        {
            "employee_id": "OFC-7491",
            "hashed_password": get_password_hash("inspectorpass"),
            "role": "Inspector",
            "full_name": "Officer Rajesh Varma",
            "jurisdiction": "Zone 4 Legal Metrology"
        },
        {
            "employee_id": "OFC-1122",
            "hashed_password": get_password_hash("fieldpass123"),
            "role": "Inspector",
            "full_name": "Field Officer Anita Desai",
            "jurisdiction": "North Zone Enforcement"
        }
    ]
    
    await users_collection.insert_many(users_to_add)
    print("Database successfully seeded with 4 users!")

asyncio.run(seed_atlas())