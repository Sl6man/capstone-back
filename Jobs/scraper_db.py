from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.snapchat_scraper
scrape_runs_collection = db.scrape_runs

def start_custom_scrape_run() -> dict:
    start_time = datetime.now()

    run_record = {
        "run_id": start_time.isoformat(),
        "start_time": start_time,
        "end_time": None,
        "locations": [],
    }

    return run_record

def finish_custom_scrape_run(run_record):
    end_time = datetime.now()
    run_record["end_time"] = end_time

    scrape_runs_collection.insert_one(run_record)
    print(f"✅ Scrape run saved with {len(run_record.get('locations', []))} locations.")
