from fastapi import APIRouter
from app.utils.random import random_uuid

from app.models.FH5.car import Car_FH5
from app.services.image import resolve_temp_image
from app.utils.time import timestamp_utc_ms

router = APIRouter(tags=["car"])


@router.get("")
async def car_indexedDB():

    carFH5s = await Car_FH5.find_all().to_list()
    return {
        "version": "abc",
        "lastUpdate": timestamp_utc_ms(),
        "data": [await carFH5.indexedDB_car() for carFH5 in carFH5s],
    }


@router.get("/image")
async def car_images_indexedDB():
    carFH5s = await Car_FH5.find_all().to_list()
    return {
        "version": "abc",
        "lastUpdate": timestamp_utc_ms(),
        "data": [carFH5.indexedDB_Images_sync() for carFH5 in carFH5s],
    }
