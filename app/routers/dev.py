from fastapi import APIRouter, Depends
from typing import Annotated
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user

router = APIRouter(prefix="/dev")


@router.get("/user")
async def get_user(current_user: Annotated[UserAuth, Depends(get_current_active_user)]):

    return current_user
