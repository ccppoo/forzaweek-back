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

from app.configs import awsSettings
import botocore
import urllib


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


@router.get("")
async def get_image():
    return "hello"


@router.post("")
async def upload_image(file: UploadFile):

    file_path = f"./uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # upload file -> 서버에서 다운 받고, 다시 보내는 방식
    # upload file object -> 클라이언트가 바이너리로 보낸 스트림을 그대로 다시 받아서 보내는 형식(저장 x)
    client_s3.upload_file(
        Filename=file_path,
        Bucket=awsSettings.BUCKET,
        Key=file.filename,
        ExtraArgs={"ContentType": file.content_type},
    )

    urllib.parse.quote(file.filename, safe="~()*!.'"),
    url = (
        f"https://s3-ap-northeast-2.amazonaws.com/{awsSettings.BUCKET}/{file.filename}"
    )

    return {"filename": url}
