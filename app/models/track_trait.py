from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal
from .i18n import i18n

__all__ = ("TrackType", "CourseType", "dbInit")


class TrackTraitName(i18n):
    # value : str
    # lang: str
    pass


class TrackTraitDescription(i18n):
    # value : str
    # lang: str
    pass


class TrackTrait(Document):

    name: TrackTraitName
    description: TrackTraitDescription

    class Settings:
        is_root = True


class TrackType(TrackTrait):
    # 로드, 오프로드, 크로스컨트리
    # name: TrackTraitName
    # description: TrackTraitDescription
    pass


class CourseType(TrackTrait):
    # 질주(스프린트), 서킷, 이벤트(골리앗, 콜로서스)
    # name: TrackTraitName
    # description: TrackTraitDescription
    pass


dbInit = (TrackTraitName, TrackTraitDescription, TrackTrait, TrackType, CourseType)
