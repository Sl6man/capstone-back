
from datetime import datetime, timezone
from pymongo import MongoClient
from sqlalchemy.orm import  Session, joinedload

from models.scraper_model import Location, Scraper
from schema.scraper_schema import LocationCreate, ScraperCreate, ScraperUpdate


class ScraperRepository:
    def __init__(self, db: Session):
        self.db = db
        client = MongoClient("mongodb://localhost:27017")
        self.db_mongo = client["snapchat_scraper"] 
            
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
    
    
    def update_scraper(self, scraper_id: int, scraper_data: ScraperUpdate):
        scraper = self.db.query(Scraper).filter(Scraper.scraper_id == scraper_id).first()
        if not scraper:
            return None

        for key, value in scraper_data.dict(exclude_unset=True).items():
            setattr(scraper, key, value)

        self.db.commit()
        self.db.refresh(scraper)
        return scraper
    
    
    def get_all_scraper(self):
        return self.db.query(Scraper).all()
    
    def get_scraper_by_id(self,scraper_id):
        return self.db.query(Scraper).options(joinedload(Scraper.locations)).filter(Scraper.scraper_id == scraper_id).first()
    
    def get_number_of_media(self, scraper_id):
        return self.db_mongo.media.count_documents({"scraper_id": scraper_id})

    
    
#-----------------delete---------------------

    def delete_scraper(self,db: Session, scraper_id: int):
        scraper = db.query(Scraper).filter(Scraper.scraper_id == scraper_id).first()
        if not scraper:
            return None
        db.delete(scraper)
        db.commit()
        return scraper