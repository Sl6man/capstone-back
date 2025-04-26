

import re
from typing import Counter


class MediaRepository:
    def __init__(self, collection):
        self.collection = collection

    async def get_media_neighborhood(self):
        pipeline = [
            {"$unwind": "$neighborhoods"},
            {
                "$group": {
                    "_id": "$neighborhoods.name",
                    "total_new_media": {"$sum": "$neighborhoods.total_new_media"},
                    "duplicate_media": {"$sum": "$neighborhoods.duplicate_media"},
                    "total_new_media_duration": {"$sum": "$neighborhoods.total_new_media_duration"},
                    "time_taken": {"$sum": "$neighborhoods.time_taken"}
                }
            },
            {"$sort": {"total_new_media": -1}},   
            {"$limit": 10},                       
            {"$sample": {"size": 10}}           
        ]


        cursor = self.collection.aggregate(pipeline)
        return [doc async for doc in cursor]
    




    async def get_top_neighborhoods_by_duration(self):
        pipeline = [
            {"$unwind": "$neighborhoods"},
            {
                "$group": {
                    "_id": "$neighborhoods.name",
                    "total_new_media_duration": {
                        "$sum": "$neighborhoods.total_new_media_duration"
                    }
                }
            },
            {"$sort": {"total_new_media_duration": -1}},
            {"$limit": 6},
            
        ]

        cursor = self.collection.aggregate(pipeline)
        return [doc async for doc in cursor]
    
    async def get_top_neighborhoods_by_duplicate(self):
        pipeline = [
            {"$unwind": "$neighborhoods"},
            {
                "$group": {
                    "_id": "$neighborhoods.name",
                    "duplicate_media": {"$sum": "$neighborhoods.duplicate_media"}
                }
            },
            {"$sort": {"total_new_media_duration": -1}},
            {"$limit": 6},
            {"$sample": {"size": 6}}
        ]

        cursor = self.collection.aggregate(pipeline)
        return [doc async for doc in cursor]
    



    
    async def get_snap_kpis(self):
        pipeline = [
            {
                "$group": {
                    "_id": "$neighborhood",
                    "count": {"$sum": 1}
                }
            }
        ]
        cursor = self.collection.aggregate(pipeline)
        neighborhood_counts = [doc async for doc in cursor]

        total_snaps = sum(n['count'] for n in neighborhood_counts)
        top_neighborhood = max(neighborhood_counts, key=lambda x: x['count'])['_id']
        lowest_neighborhood = min(neighborhood_counts, key=lambda x: x['count'])['_id']

        photo_query = {
            "$or": [
                {"snapMediaType": None},
                {"snapMediaType": "SNAP_MEDIA_TYPE_VIDEO_NO_SOUND"}
            ]
        }
        video_query = {
            "snapMediaType": "SNAP_MEDIA_TYPE_VIDEO"
        }

        total_photo = await self.collection.count_documents(photo_query)
        total_video = await self.collection.count_documents(video_query)

        return {
            "total_snaps": total_snaps,
            "top_neighborhood": top_neighborhood,
            "lowest_neighborhood": lowest_neighborhood,
            "total_photo": total_photo,
            "total_video": total_video
        }


    async def get_snaps_per_day(self):
        pipeline = [
            {
                "$addFields": {
                    "dayOfWeek": { "$dayOfWeek": { "$toDate": { "$toLong": { "$toDecimal": "$timestamp" } } } }
                }
            },
            {
                "$group": {
                    "_id": "$dayOfWeek",
                    "count": { "$sum": 1 }
                }
            }
        ]

        cursor = self.collection.aggregate(pipeline)
        data = [doc async for doc in cursor]
        
        
        day_mapping = {
            1: "Sunday",
            2: "Monday",
            3: "Tuesday",
            4: "Wednesday",
            5: "Thursday",
            6: "Friday",
            7: "Saturday"
        }

        result = []
        for item in data:
            result.append({
                "day": day_mapping.get(item["_id"], "Unknown"),
                "count": item["count"]
            })

        days_order = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        sorted_result = sorted(result, key=lambda x: days_order.index(x["day"]))    

        return sorted_result
    

    async def get_top_words(self, limit=5):
        cursor = self.collection.find({"overlay_text": {"$ne": None}}, {"overlay_text": 1})
        texts = [doc async for doc in cursor]

        words = []
        for doc in texts:
            overlay = doc.get("overlay_text", "")
            overlay = re.sub(r'[^\w\s]', '', overlay)  
            words.extend(overlay.split())

        counter = Counter(words)
        top_words = counter.most_common(limit)

        return [{"word": word, "count": count} for word, count in top_words]