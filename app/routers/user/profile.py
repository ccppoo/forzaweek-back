from fastapi import APIRouter, Depends
from typing import Annotated
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user

__all__ = ("router",)

router = APIRouter(prefix="/profile", tags=["auth"])


@router.get("")
async def get_profile(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
):

    data = {
        "gamerTag": current_user.oauth.xbox.gamer_tag,
        "profileImage": current_user.oauth.xbox.profile_image,
        "userID": current_user.user_id,
    }
    return data


@router.get("/{userID}")
async def get_user_profile(
    userID: str,
):

    user = await UserAuth.find_user_by_user_id(user_id=userID)
    if user:

        data = {
            "gamerTag": user.oauth.xbox.gamer_tag,
            "profileImage": user.oauth.xbox.profile_image,
            "userID": userID,
        }
        return data
    return "no user"
