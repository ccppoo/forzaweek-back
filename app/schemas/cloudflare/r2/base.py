from datetime import datetime
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    AliasGenerator,
    field_validator,
    model_validator,
)

# head 요청하면 반환하는 거

__all__ = ("HTTPResponseHeaderBase",)


def snake_to_dash(dashed: str) -> str:
    return dashed.replace("_", "-")


class HTTPResponseHeaderBase(BaseModel):
    connection: str = Field(description="keep-alive")
    date: datetime
    vary: str = Field(description="Accept-Encoding")
    cf_ray: str = Field(description="8aef3fe7fd463296-ICN")
    server: str = Field(description="cloudflare")

    @field_validator("date", "last_modified", mode="before", check_fields=False)
    def validate_string_date(cls, v: str | datetime) -> datetime:
        if isinstance(v, datetime):
            return v
        date_format = "%a, %d %b %Y %H:%M:%S %Z"
        parsed_date = datetime.strptime(v, date_format)
        return parsed_date

    @field_validator("etag", mode="before", check_fields=False)
    def validate_etag(cls, v: str) -> str:
        return str(v)

    @model_validator(mode="before")
    def model_key_redesign(cls, data: dict) -> dict:

        AMZ_META_HEAD_PREFIX = "x-amz"
        META_DATA = f"{AMZ_META_HEAD_PREFIX}-meta-"
        _data = {}
        for k, v in data.items():
            _k, _v = k, v
            if k.startswith(META_DATA):
                if not _data.get("meta"):
                    _data["meta"] = {}
                field_name = k.replace(f"{META_DATA}", "")
                _data["meta"][field_name] = v
            else:
                _data[_k] = _v
        return _data

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=snake_to_dash,
        )
    )
