from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("swaggerSettings",)

_description = """
Project-GP 백엔드

담당자 - 신준형 
"""


class SwaggerSettings(BaseSettings):
    title: str = "2023년 2학기 참빛설계학기, Project-GP"
    version: str = "0.0.1"
    description: str = _description
    summary: str | None = None

    ## Pydantic V2
    model_config = SettingsConfigDict()


swaggerSettings = SwaggerSettings()
