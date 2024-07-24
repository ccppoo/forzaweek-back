from __future__ import annotations
import boto3.s3
import boto3.session
import botocore.client
from fastapi import APIRouter, UploadFile, File
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field
import anyio
from typing import List, Dict, Any, Optional
import asyncio
import json
from pprint import pprint
from datetime import datetime
import boto3
from app.configs import awsSettings, runtimeSettings, cfSettings
import uuid

import botocore
import urllib
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

    temp_image_allow = ["nation", "manufacturer", "car", "tagkind", "decal", "track"]

    requestedImage = await file.read()

    if folder not in temp_image_allow:
        return 403

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
