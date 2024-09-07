from fastapi import APIRouter
from app.utils.random import random_uuid

from app.models.FH5.race_route import RaceRouteFH5
from app.utils.time import timestamp_utc_ms

router = APIRouter(tags=["race route"])


@router.get("")
async def race_route_indexedDB():

    # raceRouteFH5 = await RaceRouteFH5.get("66dc22ac8e5dc057778603af")
    # return await raceRouteFH5.indexedDB_race_route()

    raceRouteFH5s = await RaceRouteFH5.find_all().to_list()

    return {
        "version": "abc",
        "lastUpdate": timestamp_utc_ms(),
        "data": [
            await raceRouteFH5.indexedDB_race_route() for raceRouteFH5 in raceRouteFH5s
        ],
    }


@router.get("/image")
async def race_route_images_indexedDB():
    # raceRouteFH5 = await RaceRouteFH5.get("66dc22ac8e5dc057778603af")
    # return raceRouteFH5.indexedDB_Images_sync()

    raceRouteFH5s = await RaceRouteFH5.find_all().to_list()

    return {
        "version": "abc",
        "lastUpdate": timestamp_utc_ms(),
        "data": [
            raceRouteFH5.indexedDB_Images_sync() for raceRouteFH5 in raceRouteFH5s
        ],
    }
