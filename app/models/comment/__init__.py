from .comment import *
from .comments import *

__all__ = (
    "CommentsBase",
    "VotableComments",
    "TaggableComments",
    "CommentBase",
    "TagableComment",
    "VotableComment",
)

dbInit = (
    CommentsBase,
    VotableComments,
    TaggableComments,
    CommentBase,
    TaggableComment,
    VotableComment,
)
