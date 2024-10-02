from fastapi import APIRouter, Query, Depends, Body, Path

from app.models.FH5.decal import Decal as Decal_FH5, DecalImages as DecalImages_FH5

from app.models.FH5.car import Car_FH5
from app.models.tag import TagItem as TagDB
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal, Annotated
from app.types.http import Url
from pprint import pprint
from bson import ObjectId, DBRef
from app.models.FH5.decal import Decal
from app.utils.random import random_uuid
from app.services.image import resolve_temp_image
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user, get_optional_active_user

from app.services.image.file_key import promote_to_permanent
from beanie import Link


__all__ = ("router",)

router = APIRouter(prefix="", tags=["decal"])


@router.get("/{decalID}")
async def get_other_decal_like(decalID: Annotated[str, Path()]):
    # TODO:
    decalFH5 = await Decal_FH5.get(decalID)
    decalFH5s = await Decal_FH5.find(
        Decal_FH5.base_car_FH5 == decalFH5.base_car_FH5
    ).to_list()
    for decalfh5 in decalFH5s:
        print(decalfh5)
    return
