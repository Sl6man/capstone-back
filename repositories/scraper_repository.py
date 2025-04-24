
from datetime import datetime, timezone
from sqlalchemy.orm import  Session

from models.scraper_model import Location, Scraper
from schema.scraper_schema import LocationCreate, ScraperCreate


class ScraperRepository:
    def __init__(self, db: Session):
        self.db = db
            
    def create_scraper(self, scraper: ScraperCreate):
        db_scraper = Scraper(
            title=scraper.title,
            status=scraper.status,
            started_date=scraper.started_date or datetime.now(timezone.utc),
            end_date=scraper.end_date
        )
        self.db.add(db_scraper)
        self.db.commit()
        self.db.refresh(db_scraper)
        return db_scraper    
    
    
    def create_location(self, location: LocationCreate):
        db_location = Location(
            neighborhood_name=location.neighborhood_name,
            radius=location.radius,
            lat=location.lat,
            long=location.long,
            scraper_id=location.scraper_id
        )
        self.db.add(db_location)
        self.db.commit()
        self.db.refresh(db_location)
        return db_location
    
    def get_all_scraper(self):
        return self.db.query(Scraper).all()
    
    def get_scraper_by_id(self,scraper_id):
        return self.db.query(Scraper).filter(Scraper.scraper_id == scraper_id).first()