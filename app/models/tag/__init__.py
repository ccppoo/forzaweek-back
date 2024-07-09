from .tag import Tag, TagDescription, TagName
from .kind import TagKind, TagKindName, TagKindDescription

dbInit = (
    Tag,
    TagDescription,
    TagName,
    TagKind,
    TagKindName,
    TagKindDescription,
)

__all__ = (
    "dbInit",
    "Tag",
    "TagDescription",
    "TagName",
    "TagKind",
    "TagKindName",
    "TagKindDescription",
)
