from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_DETAILS)
db = client["snap_scope"]


scrape_runs_collection = db.get_collection("snapchat_riyadh.scrape_runs")
snaps_collection = db.get_collection("snapchat_riyadh.media")

