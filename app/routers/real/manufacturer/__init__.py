from fastapi import APIRouter, UploadFile, File

from .create import router as createRouter

router = APIRouter(prefix="/manufacturer", tags=["manufacturer"])

router.include_router(createRouter)
