from pydantic import BaseModel, Field

__all__ = (
    "JWTHeader",
    "JWTPayload",
)


class JWTHeader(BaseModel):
    typ: str = Field(description="type of token")
    alg: str = Field(description="Signature or encryption algorithm")
    kid: str = Field(description="Key ID")


class JWTPayload(BaseModel):
    iss: str = Field(description="JWT issuer (who created and signed this token)")
    sub: str = Field(description="JWT subject (whom the token refers to)")
    aud: str = Field(description="Audience (who or what the token is intended for)")
    exp: int = Field(description="Expiration time(seconds since Unix epoch)")
    iat: int = Field(description="Issued at (seconds since Unix epoch)")
    nbf: int = Field(description="Not Valid before (seconds since Unix epoch)")
