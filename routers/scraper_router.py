from fastapi import APIRouter, HTTPException ,Depends ,status
# from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from data.db_config import SessionLocal,engine
from sqlalchemy.orm import Session

from typing import Annotated

from schema.media_schema import Neighborhood

from schema.scraper_schema import LocationCreate, LocationRead, ScraperCreate, ScraperRead,ScraperBase, ScraperUpdate, ScraperWithLocations
from services.scraper_services import ScraperService

from data.mongo_config import scrape_runs_collection

router = APIRouter(prefix="/scraper", tags=["scraper"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/{scraper_id}', response_model=ScraperWithLocations, status_code=status.HTTP_200_OK)
async def get_scraper(scraper_id: int, db: Session = Depends(get_db)):
    scraper_service = ScraperService(db)
    return scraper_service.get_scraper_by_id(scraper_id)


@router.get('/', response_model=list[ScraperRead], status_code=status.HTTP_200_OK)
async def get_all_scrapers(db: Session = Depends(get_db)):
    scraper_service = ScraperService(db)
    return scraper_service.get_all_scrapers()


@router.post('/create', response_model=ScraperRead, status_code=status.HTTP_201_CREATED)
async def create_scraper(scraper: ScraperCreate, db: Session = Depends(get_db)):
    scraper_service = ScraperService(db)
    return scraper_service.create_scraper(scraper)


@router.put('/update/{scraper_id}', status_code=status.HTTP_200_OK)
async def update_scraper(scraper_id: int, scraper_data: ScraperUpdate, db: Session = Depends(get_db)):
    scraper_service = ScraperService(db)
    updated_scraper = scraper_service.update_scraper(scraper_id, scraper_data)
    if not updated_scraper:
        raise HTTPException(status_code=404, detail="Scraper not found")
    return updated_scraper


@router.post('/create/location', response_model=LocationRead, status_code=status.HTTP_201_CREATED)
async def create_location(location:LocationCreate, db: Session = Depends(get_db)):
    scraper_service = ScraperService(db)
    return scraper_service.create_location(location)


#-------------------delete---------------------

@router.delete("/delete/{scraper_id}")
async def delete_user(scraper_id: int, db: Session = Depends(get_db)):
    
    scraper_service = ScraperService(db)
    deleted_scraper = scraper_service.delete_scraper(db, scraper_id)
    if not deleted_scraper:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}