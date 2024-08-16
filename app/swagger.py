from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("swaggerSettings",)

_description = """
forzaweek backend
"""


class SwaggerSettings(BaseSettings):
    title: str = "forzaweek backend"
    version: str = "0.0.1"
    description: str = _description
    summary: str | None = None

    ## Pydantic V2
    model_config = SettingsConfigDict()


swaggerSettings = SwaggerSettings()
