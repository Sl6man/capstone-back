from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_DETAILS)
#db = client["snapchat_riyadh"]
db = client["snap_scope"]


scrape_runs_collection = db.get_collection("scrape_runs")
snaps_collection = db.get_collection("media")


async def check_mongo_connection():
    try:
        # 🟢 Try to ping the server
        await client.admin.command("ping")
        print("✅ Successfully connected to MongoDB!")
    except Exception as e:
        print("❌ Failed to connect to MongoDB:", e)
