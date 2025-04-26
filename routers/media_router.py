from typing import List
from fastapi import APIRouter, HTTPException ,Depends ,status

from data.mongo_config import scrape_runs_collection,snaps_collection
from services.media_services import MediaService
from schema.media_schema import Neighborhood, NeighborhoodDuplicate, NeighborhoodDuration, SnapKPISchema, SnapPerDay, TopWord
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter(prefix="/media", tags=["media"])

def get_scrape_runs_collection() -> AsyncIOMotorCollection:
    return scrape_runs_collection

def get_scrape_collection() -> AsyncIOMotorCollection:
    return snaps_collection

@router.get('/neighborhood',response_model=List[Neighborhood],status_code=status.HTTP_200_OK)
async def get_media_neighborhood(collection=Depends(get_scrape_runs_collection)):
    media_service=MediaService(scrape_runs_collection)
    return await media_service.get_media_neighborhood()


@router.get("/neighborhood/duration", response_model=List[NeighborhoodDuration], status_code=status.HTTP_200_OK)
async def get_top_neighborhoods_by_duration(collection=Depends(get_scrape_runs_collection)):
    media_service = MediaService(collection)
    return await media_service.get_top_neighborhoods_by_duration()

@router.get('/neighborhood/duplicates', response_model=List[NeighborhoodDuplicate], status_code=status.HTTP_200_OK)
async def get_top_duplicates(collection=Depends(get_scrape_runs_collection)):
    media_service = MediaService(collection)
    return await media_service.get_top_neighborhoods_by_duplicate()



@router.get('/kpis', response_model=SnapKPISchema, status_code=status.HTTP_200_OK)
async def get_snaps_kpis(collection=Depends(get_scrape_collection)):
    service = MediaService(collection)
    return await service.get_snap_kpis()


@router.get("/snaps/weekdays", response_model=List[SnapPerDay], status_code=status.HTTP_200_OK)
async def get_snaps_per_day(collection=Depends(get_scrape_collection)):
    service = MediaService(collection)
    return await service.get_snaps_per_day()


@router.get("/words", response_model=List[TopWord], status_code=status.HTTP_200_OK)
async def get_top_words(collection=Depends(get_scrape_collection)):
    service = MediaService(collection)
    return await service.get_top_words()