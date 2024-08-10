from app.models.user import UserAuth
from app.models.tag import Tag
from fastapi import APIRouter, Depends, Query, Path
from typing import Annotated, Optional, Literal, List
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user, get_optional_active_user
from pprint import pprint
from pydantic import BaseModel, field_validator, Field
from beanie.odm.fields import PydanticObjectId

router = APIRouter(prefix="")


@router.get("/{board_name}/{post_id}")
async def get_board_post(board_name: str, post_id: int):
    print(f"{board_name=} {post_id=}")

    return {}
