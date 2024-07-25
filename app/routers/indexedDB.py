from __future__ import annotations
from fastapi import APIRouter
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
from pprint import pprint
from datetime import datetime
from bson import ObjectId
from beanie import WriteRules, DeleteRules


from app.models.car import (
    Car as CarDB,
    CarName,
    CarShortName,
)
from app.models.track.fh5 import Track_FH5

from app.models.car import Car as CarDB
from app.models.manufacturer import Manufacturer as ManufacturerDB
from app.models.nation import Nation as NationDB
from app.utils.random import random_uuid
import asyncio

from app.services.image import resolve_temp_image
from app.utils.time import timestamp_utc_ms

router = APIRouter(prefix="/db", tags=["indexedDB", "car", "manufacturer"])


@router.get("/car2")
async def get_all_cars():
    # Car DB 프런트에 맞게 보내주기
    cars = await CarDB.find_all().to_list()

    [await car.fetch_all_links() for car in cars]

    a = [car.indexedDB_car() for car in cars]
    utc_ms = timestamp_utc_ms()
    return {"version": f"{utc_ms}", "lastUpdate": utc_ms, "data": a}


@router.get("/car2/fh5/meta")
async def get_all_cars_fh5_meta():
    # Car DB 프런트에 맞게 보내주기
    # FH5에서 희귀도, 가격
    cars = await CarDB.find({"fh5": {"$ne": None}}).to_list()

    [await car.fetch_all_links() for car in cars]

    a = [car.indexedDB_fh5_meta() for car in cars]
    utc_ms = timestamp_utc_ms()
    return {"version": f"{utc_ms}", "lastUpdate": utc_ms, "data": a}


@router.get("/car2/fh5/performance")
async def get_all_cars_fh5_performance():
    # Car DB 프런트에 맞게 보내주기
    # FH5에서 희귀도, 가격
    cars = await CarDB.find({"fh5": {"$ne": None}}).to_list()

    [await car.fetch_all_links() for car in cars]

    a = [car.indexedDB_fh5_performance() for car in cars]
    utc_ms = timestamp_utc_ms()
    return {"version": f"{utc_ms}", "lastUpdate": utc_ms, "data": a}


@router.get("/car2/image")
async def get_all_cars_images():
    # Car DB 프런트에 맞게 보내주기
    cars = await CarDB.find_all().to_list()

    [await car.fetch_all_links() for car in cars]

    a = [car.indexedDB_images() for car in cars]
    utc_ms = timestamp_utc_ms()
    return {"version": f"{utc_ms}", "lastUpdate": utc_ms, "data": a}


@router.get("/nation")
async def get_nation_db():

    nations = await NationDB.find_all().to_list()
    [await nation.fetch_all_links() for nation in nations]

    a = [nation.to_indexedDB() for nation in nations]
    utc_ms = timestamp_utc_ms()
    return {"version": f"{utc_ms}", "lastUpdate": utc_ms, "data": a}


@router.get("/manufacturer")
async def get_manufacturer_db():

    manufacturers = await ManufacturerDB.find_all().to_list()
    [await manufacturer.fetch_all_links() for manufacturer in manufacturers]

    a = [manufacturer.to_indexedDB() for manufacturer in manufacturers]
    utc_ms = timestamp_utc_ms()
    return {"version": f"{utc_ms}", "lastUpdate": utc_ms, "data": a}


@router.get("/track2")
async def get_track_db():
    tracks = await Track_FH5.find_all().to_list()
    [await t.fetch_all_links() for t in tracks]
    a = [t.to_indexedDB() for t in tracks]
    utc_ms = timestamp_utc_ms()

    return {"version": f"{utc_ms}", "lastUpdate": utc_ms, "data": a}


@router.get("/track2/image")
async def get_track_image_db():

    tracks = await Track_FH5.find_all().to_list()
    [await t.fetch_all_links() for t in tracks]
    a = [t.to_indexedDB_image() for t in tracks]
    utc_ms = timestamp_utc_ms()

    return {"version": f"{utc_ms}", "lastUpdate": utc_ms, "data": a}
