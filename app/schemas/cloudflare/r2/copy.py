from datetime import datetime
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)
from .base import HTTPResponseHeaderBase

__all__ = (
    "ObjectCopyResponseMetadata",
    "CopyObjectResult",
    "R2_object_copy_response",
)


class R2_CopyRequestReponseMetaHeader(BaseModel):
    copy_source_version_id: str
    version_id: str


class HTTPCopyRequestResponseHeader(HTTPResponseHeaderBase):

    content_length: int = Field()
    content_type: str = Field(description="image/jpg")
    meta: R2_CopyRequestReponseMetaHeader

    @model_validator(mode="before")
    def model_key_redesign2(cls, data: dict) -> dict:

        AMZ_HEAD_PREFIX = "x-amz-"

        _data = {}
        for k, v in data.items():
            _k, _v = k, v
            if k.startswith(AMZ_HEAD_PREFIX):
                if not _data.get("meta"):
                    _data["meta"] = {}
                field_name = k.replace(f"{AMZ_HEAD_PREFIX}", "").replace("-", "_")
                _data["meta"][field_name] = v
            else:
                _data[_k] = _v
        return _data


class ObjectCopyResponseMetadata(BaseModel):
    HTTPHeaders: HTTPCopyRequestResponseHeader
    HTTPStatusCode: int = Field(ge=100, description="success : 200")
    RetryAttempts: int = Field(ge=0)


class CopyObjectResult(BaseModel):
    ETag: str
    LastModified: datetime


class R2_object_copy_response(BaseModel):
    ResponseMetadata: ObjectCopyResponseMetadata
    VersionId: str
    CopySourceVersionId: str
    CopyObjectResult: CopyObjectResult
