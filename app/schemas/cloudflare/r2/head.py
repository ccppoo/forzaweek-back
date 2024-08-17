from datetime import datetime
from pydantic import BaseModel, Field
from .base import HTTPResponseHeaderBase
from app.schemas.cloudflare.object_meta import R2_ObjectMetaData


__all__ = (
    "HTTPHeadRequestResponseHeader",
    "HeadResponseMetadata",
    "R2_object_head_response",
)


class HTTPHeadRequestResponseHeader(HTTPResponseHeaderBase):
    accept_ranges: str = Field(description="bytes")
    content_length: int = Field()
    content_type: str = Field(description="image/jpg")
    etag: str
    last_modified: datetime
    meta: R2_ObjectMetaData


class HeadResponseMetadata(BaseModel):
    HTTPHeaders: HTTPHeadRequestResponseHeader
    HTTPStatusCode: int
    RetryAttempts: int = Field(ge=0)


class R2_object_head_response(BaseModel):
    AcceptRanges: str = Field(description="bytes")
    ContentLength: int = Field(ge=0, description="length of bytes")
    ContentType: str = Field(description='ex : "image/jpg"')
    ETag: str
    LastModified: datetime
    Metadata: R2_ObjectMetaData
    ResponseMetadata: HeadResponseMetadata
