import asyncio
import random
from datetime import datetime, timezone
from pymongo import MongoClient

# Setup Mongo connection
client = MongoClient("mongodb://localhost:27017")
db = client.snapchat_scraper
media_collection = db.media
scrape_runs_collection = db.scrape_runs

# Helper function to generate dummy snap
def generate_dummy_snap(location, scraper_id):
    now = datetime.now(timezone.utc)
    return {
        "id": f"snap_{random.randint(100000, 999999)}",
        "coordinates": [location["lat"], location["long"]],
        "timestamp": now.isoformat(),
        "duration_seconds": random.choice([10, 15, 30]),
        "snapMediaType": random.choice(["video", "image"]),
        "title": f"Snap at {location['lat']:.2f},{location['long']:.2f}",
        "created_at": now.isoformat(),
        "last_scraped_at": now.isoformat(),
        "scraper_id": scraper_id
    }

# Simulate scraping locations
def simulate_scrape(locations, scraper_id):
    new_snaps = []
    for loc in locations:
        count = random.randint(1, 5)
        for _ in range(count):
            snap = generate_dummy_snap(loc, scraper_id)
            media_collection.insert_one(snap)
            new_snaps.append(snap)
    return new_snaps

# Main background task
async def background_scraper(start_date: datetime, end_date: datetime, params: dict):
    now = datetime.now(timezone.utc)

    if now < start_date:
        wait_seconds = (start_date - now).total_seconds()
        print(f"\u23f3 Waiting {wait_seconds:.2f} seconds until start...")
        await asyncio.sleep(wait_seconds)

    print("\U0001f7e2 Simulated scraping started!")

    run_record = {
        "run_id": datetime.now().isoformat(),
        "start_time": datetime.now(),
        "locations": [],
        "end_time": None,
    }

    while datetime.now(timezone.utc) < end_date:
        try:
            locations = params.get("locations", [])
            if not locations:
                print("\u26a0\ufe0f No locations provided to scrape.")
                break

            new_snaps = simulate_scrape(locations, params.get('scraper_id'))
            run_record["locations"].extend(new_snaps)

            print(f"\u2705 Generated {len(new_snaps)} dummy snaps")
            await asyncio.sleep(600)  # Wait 10 minutes between cycles

        except Exception as e:
            print(f"Error during simulated scraping: {e}")
            break

    run_record["end_time"] = datetime.now()
    scrape_runs_collection.insert_one(run_record)
    print("\U0001f534 Simulated scraping stopped (end time reached)")
