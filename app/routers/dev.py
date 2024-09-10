from fastapi import APIRouter, Depends
from typing import Annotated
from app.models.user.UserAuth import UserAuth
from app.models.i18n import i18n
from app.services.auth.deps import get_current_active_user
from app.models.country import Country
from beanie import DeleteRules
from beanie.odm.fields import PydanticObjectId
from app.models.FH5.race_route.i18n import RaceRouteName
from app.models.FH5.race_route import RaceRouteFH5

router = APIRouter(prefix="/dev", tags=["dev"])


@router.get("/user")
async def get_user(current_user: Annotated[UserAuth, Depends(get_current_active_user)]):

    return current_user


@router.post("/temp")
async def temp_route():
    print()
    raceRouteNames = await RaceRouteName.find_all().to_list()
    for r in raceRouteNames:
        await r.delete()
