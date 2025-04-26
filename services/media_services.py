from repositories.media_repositroy import MediaRepository
from schema.media_schema import Neighborhood, NeighborhoodDuplicate, NeighborhoodDuration, SnapPerDay, TopWord

class MediaService:
    def __init__(self, collection):
        self.repository = MediaRepository(collection)

    async def get_media_neighborhood(self):
        data = await self.repository.get_media_neighborhood()
        validated_data = []

        for item in data:
            try:
                item["name"] = item.pop("_id")
                neighborhood = Neighborhood(**item)
                validated_data.append(neighborhood)
            except Exception as e:
                print(f"Invalid neighborhood data skipped: {e}")

        return validated_data
    



    async def get_top_neighborhoods_by_duration(self):
        data = await self.repository.get_top_neighborhoods_by_duration()
        validated = []

        for item in data:
            try:
                validated.append(
                    NeighborhoodDuration(
                        name=item["_id"],
                        total_new_media_duration=int(item["total_new_media_duration"])  
                    )
                )
            except Exception as e:
                print(f"Invalid data skipped: {e}")

        return validated
    


    async def get_top_neighborhoods_by_duplicate(self):
        data = await self.repository.get_top_neighborhoods_by_duplicate()
        validated = []

        for item in data:
            try:
                validated.append(
                    NeighborhoodDuplicate(
                        name=item["_id"],
                        duplicate_media=int(item["duplicate_media"])
                    )
                )
            except Exception as e:
                print(f"Invalid data skipped: {e}")

        return validated
    



    async def get_snap_kpis(self):
        return await self.repository.get_snap_kpis()
    
    async def get_snaps_per_day(self):
        data = await self.repository.get_snaps_per_day()
        return [SnapPerDay(**item) for item in data]
    

    async def get_top_words(self):
        data = await self.repository.get_top_words()
        return [TopWord(**item) for item in data]