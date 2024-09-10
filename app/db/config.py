from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import init_beanie

from app.configs import dbSettings
from app.models import models
import asyncio

mongodb: AsyncIOMotorDatabase = None


async def start_up_db(app: FastAPI):
    app.db = AsyncIOMotorClient(dbSettings.URL)[dbSettings.DATABASE]
    await init_beanie(
        app.db,
        document_models=models,
    )


async def check_connection(timeout: float = 3) -> bool:
    try:
        global mongodb
        mongodb = AsyncIOMotorClient(dbSettings.URL)[dbSettings.DATABASE]
        await mongodb.list_collections()
    except asyncio.TimeoutError:
        return False
    else:
        return True


async def get_db_async():
    return AsyncIOMotorClient(dbSettings.URL)
