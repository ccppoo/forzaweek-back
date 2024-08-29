from __future__ import annotations
from fastapi import APIRouter, UploadFile, File

from .create import router as createRouter

router = APIRouter(prefix="/country", tags=["country"])

router.include_router(createRouter)
