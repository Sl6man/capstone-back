from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

from Jobs.scraper_db import finish_custom_scrape_run, start_custom_scrape_run
from Jobs.scraper_functions import scrape_location_task

async def scrape_given_locations(locations: list):
    folder = Path('snapchat_data')
    folder.mkdir(parents=True, exist_ok=True)

    run_record = start_custom_scrape_run()

    print(f"Starting scrape run for {len(locations)} locations")

    loop = asyncio.get_event_loop()

    def scrape_all_locations():
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(
                    scrape_location_task,
                    (folder, f"location_{i}", loc["lat"], loc["long"], 15, run_record)
                )
                for i, loc in enumerate(locations)
            ]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in future: {str(e)}")

    await loop.run_in_executor(None, scrape_all_locations)

    finish_custom_scrape_run(run_record)

    print(f"✅ Scrape completed for selected locations.")
