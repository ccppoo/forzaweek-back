from pydantic import BaseModel
from typing import Literal

__all__ = ("TrackCategory",)


class TrackCategory(BaseModel):
    # 크로스컨트리, 랠리, 온로드, 오프로드, 스트리트, 드래그
    category: Literal["cross_country", "rally", "off_road", "road", "street", "drag"]
