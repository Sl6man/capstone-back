from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class BaseNeighborhood(BaseModel):
    name: str
    total_new_media: int
    duplicate_media: int
    total_new_media_duration: float
    time_taken: float


class Neighborhood(BaseModel):
    name: str
    total_new_media: int

class NeighborhoodDuration(BaseModel):
    name: str
    total_new_media_duration: float

class NeighborhoodDuplicate(BaseModel):
    name: str
    duplicate_media: int    

class SnapKPISchema(BaseModel):
    total_snaps: int
    top_neighborhood: str | None
    lowest_neighborhood: str | None
    total_photo: int
    total_video: int


class TopWord(BaseModel):
    word: str
    count: int    

class SnapPerDay(BaseModel):
    day: str
    count: int    

class SnapDataSchema(BaseModel):
    run_id: str
    start_time: datetime
    end_time: datetime
    neighborhoods: List[Neighborhood]

    class Config:
        from_attributes = True
 