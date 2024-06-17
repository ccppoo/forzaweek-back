from typing import Annotated, Any, Optional
from pydantic import HttpUrl, TypeAdapter, BeforeValidator

from typing import Literal, List

__all__ = ("Url",)

http_url_adapter = TypeAdapter(HttpUrl)

Url = Annotated[
    str, BeforeValidator(lambda value: str(http_url_adapter.validate_python(value)))
]
