from __future__ import annotations
import boto3.s3
import boto3.session
import botocore.client
from fastapi import APIRouter, UploadFile, File, Query, Depends, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Annotated
from pprint import pprint
from datetime import datetime
import boto3
from app.configs import awsSettings, runtimeSettings, cfSettings
import uuid
from app.services.image import resolve_temp_image, delete_uploade_image
from app.services.auth.deps import get_current_active_user
from app.models.user import UserAuth

import botocore
import pathlib


router = APIRouter(prefix="/image", tags=["image"])


client_s3 = boto3.client(
    "s3",
    awsSettings.REGION,
    aws_access_key_id=awsSettings.CREDENTIALS_ACCESS_KEY,
    aws_secret_access_key=awsSettings.CREDENTIALS_SECRET_KEY,
)


class ImageURLRequest(BaseModel):
    # meditationIdx: int
    images: List[str]


@router.post("/{folder}")
async def add_nation_flag(folder: str, file: UploadFile):
    # TODO: 파일 업로드하고 사용 안된 임시파일 삭제하기

    temp_image_allow = [
        "nation",
        "manufacturer",
        "car",
        "tagkind",
        "decal",
        "track",
        "board",
    ]

    if folder not in temp_image_allow:
        return 403

    requestedImage = await file.read()

    fname = pathlib.Path(file.filename)
    _, file_ext = fname.stem, fname.suffix

    random_name = uuid.uuid4()
    temp_file_name = f"{random_name}{file_ext}"
    base_dir = runtimeSettings.TEMPFILE_BASE_DIR
    fname_temp = pathlib.Path(base_dir, "uploads", folder, temp_file_name).resolve()

    with open(fname_temp, "wb") as f:
        f.write(requestedImage)

    # 임시 저장한 파일 이름 다시 보내기 (어차피 경로는 POST : /nation으로 오니깐)
    # print(f"temp_file_name : {temp_file_name}")
    return {"image": temp_file_name}


class BoardImageDeleteRequest(BaseModel):
    url: str  # url like https://cdn.forzaweek.***


# https://fzwcdn.forzaweek.com/board/board/test/d7546921-188e-474e-bce8-4f872dfcec76.jpg
@router.post("/board/upload")
async def upload_image_from_board(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    file: UploadFile,
):
    # TODO: 파일 업로드하고 사용 안된 임시파일 삭제하기

    print(f"current_user : {current_user.oauth.xbox.gamer_tag}")
    temp_image_allow = [
        "board",
    ]
    folder = "board"
    requestedImage = await file.read()

    fname = pathlib.Path(file.filename)
    _, file_ext = fname.stem, fname.suffix

    random_name = uuid.uuid4()
    temp_file_name = f"{random_name}{file_ext}"
    base_dir = runtimeSettings.TEMPFILE_BASE_DIR
    fname_temp = pathlib.Path(base_dir, "uploads", folder, temp_file_name).resolve()

    with open(fname_temp, "wb") as f:
        f.write(requestedImage)

    random_name = str(uuid.uuid4())

    cfURL = resolve_temp_image(
        "board", temp_file_name, random_name, current_user, "board", "test"
    )
    # 임시 저장한 파일 이름 다시 보내기 (어차피 경로는 POST : /nation으로 오니깐)
    # print(f"temp_file_name : {temp_file_name}")
    return {
        "success": 1,
        "file": {
            "url": cfURL,
        },
    }
    # return {"image": temp_file_name}


@router.post("/board/delete")
async def delete_image_from_board(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    delete_request: Annotated[BoardImageDeleteRequest, Body()],
):
    # TODO: 파일 업로드하고 사용 안된 임시파일 삭제하기
    print(f"current_user : {current_user.oauth.xbox.gamer_tag}")

    pprint(delete_request)
    # 1. 삭제 요청을 보내고 CF 에서 HEAD 요청 받아옴 -> 검증 -> 샂게
    # 1. 삭제 요청을
    cfURL = delete_uploade_image(delete_request.url, current_user)
    # 임시 저장한 파일 이름 다시 보내기 (어차피 경로는 POST : /nation으로 오니깐)
    # print(f"temp_file_name : {temp_file_name}")
    return
    return {
        "success": 1,
        "file": {
            "url": cfURL,
        },
    }
    # return {"image": temp_file_name}
