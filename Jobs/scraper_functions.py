# app/services/scraper_functions.py

import json
import pathlib
import time
from datetime import datetime
from typing import Optional, Tuple
from shapely.geometry import Point, Polygon
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# 🛠 Connect to MongoDB once
client = MongoClient('mongodb://localhost:27017/')
db = client['snapchat_scraper']

media_collection = db['media']
scrape_runs_collection = db['scrape_runs']

# 🛠 Make sure indexes exist
media_collection.create_index([("id", 1)], unique=True)
scrape_runs_collection.create_index([("run_id", 1)], unique=True)

EARTH_RADIUS = 6371000  # meters

def get_latest_tileset() -> dict:
    url = 'https://ms.sc-jpl.com/web/getLatestTileSet'
    headers = {'content-type': 'application/json'}
    resp = requests.post(url, headers=headers, json={}, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_epoch() -> int:
    try:
        tiles = get_latest_tileset()
        for t in tiles['tileSetInfos']:
            if t['id']['type'] == 'HEAT':
                return int(t['id']['epoch'])
        return 0
    except Exception as e:
        print(f"Error getting tileset: {e}")
        return 0

def download_file(file: pathlib.Path, url: str) -> None:
    if file.exists():
        return
    try:
        with requests.get(url, stream=True) as resp:
            resp.raise_for_status()
            with open(str(file), 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"Error downloading file: {e}")

def get_title(info: dict, default: str) -> str:
    titles = info.get('title', {}).get('strings')
    if titles:
        title = next((t.get('text') for t in titles if t.get('locale') == 'en'), None)
        if title:
            return title
    return info.get('title', {}).get('fallback') or default

def get_media_urls(info: dict) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    media = info.get('streamingMediaInfo')
    if media:
        prefix = media.get('prefixUrl', '')
        return (
            prefix + media['previewUrl'] if media.get('previewUrl') else None,
            prefix + media['mediaUrl'] if media.get('mediaUrl') else None,
            prefix + media['overlayUrl'] if media.get('overlayUrl') else None
        )
    return None, None, None

def scrape_location(folder: pathlib.Path, location_id: str, latitude: float, longitude: float, zoom: float = 15, epoch: Optional[int] = None) -> dict:
    if epoch is None:
        epoch = get_epoch()
    if epoch == 0:
        print('No valid epoch, skipping')
        return {}

    data = {
        "requestGeoPoint": {"lat": latitude, "lon": longitude},
        "zoomLevel": zoom,
        "tileSetId": {"flavor": "default", "epoch": epoch, "type": 1},
        "radiusMeters": 1000.0,
        "maximumFuzzRadius": 0
    }

    headers = {'Content-Type': 'application/json'}
    url = 'https://ms.sc-jpl.com/web/getPlaylist'

    try:
        resp = requests.post(url, json=data, headers=headers)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error requesting media: {e}")
        return {}

    j = resp.json()

    result = {
        "new_records": 0,
        "duplicates": 0,
        "media_types": {},
        "total_duration": 0
    }

    for vid in j['manifest']['elements']:
        idnum = vid['id']

        if media_collection.find_one({'id': idnum}):
            result["duplicates"] += 1
            media_collection.update_one(
                {'id': idnum},
                {'$set': {'last_scraped_at': datetime.now().isoformat()}}
            )
            continue

        info = vid['snapInfo']
        preview_url, media_url, overlay_url = get_media_urls(info)
        title = get_title(info, idnum)
        snapMediaType = info.get('snapMediaType')

        media_record = {
            'id': idnum,
            'duration_seconds': vid.get('duration'),
            'timestamp': vid.get('timestamp'),
            'title': title,
            'snapMediaType': snapMediaType,
            "coordinates": [latitude, longitude],
            "created_at": datetime.now().isoformat(),
            "last_scraped_at": datetime.now().isoformat()
        }

        try:
            media_collection.insert_one(media_record)
            result["new_records"] += 1
            if snapMediaType:
                result["media_types"][snapMediaType] = result["media_types"].get(snapMediaType, 0) + 1
            result["total_duration"] += vid.get('duration') or 0
        except DuplicateKeyError:
            result["duplicates"] += 1

    return result

def scrape_location_task(args):
    try:
        db_folder, location_id, lat, lon, zoom, run_record = args
        print(f"Scraping {location_id} at {lat},{lon}")

        start = time.time()

        stats = scrape_location(db_folder, location_id, lat, lon, zoom)

        time_taken = time.time() - start

        run_record["locations"].append({
            "location_id": location_id,
            "latitude": lat,
            "longitude": lon,
            "new_records": stats.get("new_records", 0),
            "duplicates": stats.get("duplicates", 0),
            "total_duration_seconds": stats.get("total_duration", 0),
            "media_types": stats.get("media_types", {}),
            "time_taken_seconds": time_taken
        })

    except Exception as e:
        print(f"Error scraping location: {str(e)}")
