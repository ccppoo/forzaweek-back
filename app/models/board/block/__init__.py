from .header import HeaderBlockData
from .nestedList import NestedListBlockData
from .paragraph import ParagraphBlockData
from .image import ImageBlockData
from typing import Union

__all__ = (
    "HeaderBlockData",
    "NestedListBlockData",
    "ParagraphBlockData",
    "ImageBlockData",
    "BlockDataTypes",
)

BlockDataTypes = Union[
    HeaderBlockData, NestedListBlockData, ParagraphBlockData, ImageBlockData
]
