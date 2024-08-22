from fastapi import APIRouter
from .tag import router as tagRouter, get_all_tags
from .category import router as tagCategoryRouter
from .tagging import router as taggingRouter
from .tags import router as tagsRouter

router = APIRouter(prefix="/tag", tags=["tag"])

router.include_router(tagRouter)
router.add_api_route("", get_all_tags)
router.include_router(tagCategoryRouter)
router.include_router(taggingRouter)
router.include_router(tagsRouter)
