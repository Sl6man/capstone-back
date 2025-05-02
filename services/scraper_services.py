import asyncio
from sqlalchemy.orm import Session

from Jobs.scraper_runner import background_scraper
from repositories.scraper_repository import ScraperRepository
from schema.scraper_schema import LocationCreate, ScraperCreate,ScraperBase


class ScraperService:
    def __init__(self, db:Session):
        self.db=db
        self.repository = ScraperRepository(db)
        
    def create_scraper(self, scraper:ScraperCreate):
        return self.repository.create_scraper(scraper)
    
    def create_location(self, location: LocationCreate):
        location_returned = self.repository.create_location(location)
        
        if location_returned:
            params = {
                "scraper_id": location_returned.scraper_id,
                "locations": [
                    {
                        "lat": location_returned.lat,
                        "long": location_returned.long,
                        "radius": location_returned.radius
                    }
                ]
            }

            # Assume you load scraper info from DB using scraper_id
            scraper_info = self.repository.get_scraper_by_id(location_returned.scraper_id)

            asyncio.create_task(
                background_scraper(scraper_info.started_date, scraper_info.end_date, params)
            )

        return location_returned

    def get_scraper_by_id(self, scraper_id: int):
        scraper_data = self.repository.get_scraper_by_id(scraper_id)
        media_collected = self.repository.get_number_of_media(scraper_id)

        if not scraper_data:
            return None

        # Convert SQLAlchemy object to dict safely
        scraper_dict = {
            key: value for key, value in scraper_data.__dict__.items()
            if key != "_sa_instance_state"
        }

        # Add media count
        scraper_dict["media_count"] = media_collected

        return scraper_dict

    
    def get_all_scrapers(self):
        return self.repository.get_all_scraper()
