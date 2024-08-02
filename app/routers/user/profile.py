from fastapi import APIRouter, Depends
from typing import Annotated
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user, optional_auth_dependent

__all__ = ("router",)

router = APIRouter(prefix="/profile", tags=["auth"])


@router.get("/{userID}")
async def get_user_profile(
    userID: str,
):

    user = await UserAuth.find_user_by_user_id(user_id=userID)
    if user:

        data = {
            "gamerTag": user.oauth.xbox.gamer_tag,
            "profileImage": user.oauth.xbox.profile_image,
        }
        return data
    return "no user"
