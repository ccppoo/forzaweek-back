import boto3
from app.configs import cfSettings

__all__ = ("client_r2",)

client_r2 = boto3.client(
    service_name="s3",
    endpoint_url=cfSettings.R2_ENDPOINT,
    aws_access_key_id=cfSettings.ACCESS_KEY,
    aws_secret_access_key=cfSettings.SECRET_ACCESS_KEY,
    region_name=cfSettings.LOCATION,
)
