from sqlalchemy.orm import Session

from repositories.scraper_repository import ScraperRepository
from schema.scraper_schema import LocationCreate, ScraperCreate,ScraperBase


class ScraperService:
    def __init__(self, db:Session):
        self.db=db
        self.repository = ScraperRepository(db)
        
    def create_scraper(self, scraper:ScraperCreate):
        
        return self.repository.create_scraper( scraper)
    
    def create_location(self, location:LocationCreate):
        
        return self.repository.create_location(location)
    

    def get_scraper_by_id(self,scraper_id:int):

        scraper_full_info=self.repository.get_scraper_by_id(scraper_id)
        scarper=ScraperBase(
            title=scraper_full_info.title,
            status=scraper_full_info.status,
            started_date=scraper_full_info.started_date,
            end_date=scraper_full_info.end_date
        )
        return scarper
    
    def get_all_scrapers(self):
        return self.repository.get_all_scraper()
