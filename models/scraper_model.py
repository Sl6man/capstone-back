from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from data.db_config import Base
from datetime import datetime, timezone
    
    
class Scraper(Base):
    __tablename__ = "scraper"

    scraper_id = Column(Integer, primary_key=True, autoincrement=True)    
    title=Column(String,unique=False,nullable=False)
    status=Column(Boolean,nullable=False)
    
    started_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)        
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    
    
    
class Location(Base):
    __tablename__ = 'location'
    
    location_id = scraper_id = Column(Integer, primary_key=True, autoincrement=True)    
    neighborhood_name = Column(String)
    radius=Column(Float, nullable=False)
    lat=Column(Float, nullable=False)
    long=Column(Float, nullable=False)
    
    scraper_id = Column(Integer, ForeignKey('scraper.scraper_id'), nullable=True)
    
    scraper = relationship('Scraper')