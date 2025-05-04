from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ---------- SCRAPER SCHEMAS ----------

class ScraperBase(BaseModel):
    title: str
    status: bool
    started_date: datetime
    end_date: datetime    
    
class ScraperCreate(ScraperBase):
    pass
class ScraperRead(ScraperBase):
    scraper_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# ---------- LOCATION SCHEMAS ----------

class LocationBase(BaseModel):
    neighborhood_name: Optional[str] = None
    radius: float
    lat: float
    long: float
    scraper_id: Optional[int] = None
    
    class Config:
        orm_mode = True 


class LocationCreate(LocationBase):
    pass


class LocationRead(LocationBase):
    location_id: int

    class Config:
        orm_mode = True


class ScraperWithLocations(ScraperBase):
    scraper_id: int
    created_at: datetime
    updated_at: datetime
    locations: list[LocationBase] = []
    media_count: int
    
    class Config:
        orm_mode = True 
        

class ScraperUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[bool] = None
    started_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    class Config:
        orm_mode = True