from pydantic import BaseModel, Field
from .base import HTTPResponseHeaderBase

__all__ = (
    "ObjectDeleteResponseMetadata",
    "R2_object_delete_response",
)


class ObjectDeleteResponseMetadata(BaseModel):
    HTTPHeaders: HTTPResponseHeaderBase
    HTTPStatusCode: int
    RetryAttempts: int = Field(ge=0)


class R2_object_delete_response(BaseModel):
    ResponseMetadata: ObjectDeleteResponseMetadata

    @property
    def is_success(self) -> bool:
        return self.ResponseMetadata.HTTPStatusCode == 204
