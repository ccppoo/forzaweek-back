from .comment import *
from .comments import *

__all__ = (
    "CommentsBase",
    "VotableComments",
    "CommentBase",
    "VotableSubComment",
    "VotableMainComment",
)

dbInit = (
    CommentsBase,
    CommentBase,
    VotableComments,
    VotableMainComment,
    VotableSubComment,
)
