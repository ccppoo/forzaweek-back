from pydantic import BaseModel
from typing import Optional
from app.types.http import Url

__all__ = ("TrackFullPathImage",)


class FullPathImage(BaseModel):
    zoom_out: Optional[Url]
    zoom_in: Optional[Url]


class TrackFullPathImage(BaseModel):
    # 크로스컨트리, 랠리, 온로드, 오프로드, 스트리트, 드래그

    fullPathImage: FullPathImage
