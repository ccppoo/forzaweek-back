from app.models.deps.system import HasMultipleImages

from ..base import FH5DocumentBase
from beanie import Link
from pydantic import BaseModel, Field
from typing import List
from .i18n import CustomMapDescription, CustomMapName


class CustomMapBase(HasMultipleImages, FH5DocumentBase):

    name: List[Link[CustomMapName]] = Field([])
    description: List[Link[CustomMapDescription]] = Field([])

    class Settings:
        name = "FH5.CustomMapBase"
        is_root = True
