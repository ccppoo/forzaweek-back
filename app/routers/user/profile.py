from fastapi import APIRouter, Depends
from typing import Annotated
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user

__all__ = ("router",)

router = APIRouter(prefix="/profile", tags=["auth"])


@router.get("")
async def get_user_profile(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)]
):

    return {
        "gamerTag": current_user.oauth.xbox.gamer_tag,
        "profileImage": current_user.oauth.xbox.profile_image,
    }
