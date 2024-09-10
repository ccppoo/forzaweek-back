from pydantic import Field, BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel, to_snake


class HTTPSchemaBase(BaseModel):

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake, serialization_alias=to_camel
        )
    )
