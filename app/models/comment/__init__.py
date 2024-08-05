from .comment import *
from .comments import *

__all__ = (
    "CommentsBase",
    "VotableComments",
    "TaggableComments",
    "CommentBase",
    "TagableComment",
    "VotableSubComment",
    "VotableMainComment",
)

dbInit = (
    CommentsBase,
    CommentBase,
    TaggableComments,
    TaggableComment,
    VotableComments,
    VotableMainComment,
    VotableSubComment,
)
