from sqlalchemy.orm import Session

from repositories.scraper_repository import ScraperRepository
from schema.scraper_schema import LocationCreate, ScraperCreate


class ScraperService:
    def __init__(self, db:Session):
        self.db=db
        self.repository = ScraperRepository(db)
        
    def create_scraper(self, scraper:ScraperCreate):
        
        return self.repository.create_scraper( scraper)
    
    def create_location(self, location:LocationCreate):
        
        return self.repository.create_location(location)