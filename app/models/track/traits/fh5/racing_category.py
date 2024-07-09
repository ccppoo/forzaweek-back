from pydantic import BaseModel
from typing import Literal

__all__ = ("RaceCategory",)


class RaceCategory(BaseModel):
    # 크로스컨트리, 랠리, 온로드, 오프로드, 스트리트, 드래그
    category_name: Literal[
        "cross country", "rally", "off-road", "on-road", "street", "drag"
    ]
