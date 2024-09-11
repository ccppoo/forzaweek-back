import boto3
from app.configs import cfSettings
from types_aiobotocore_s3.client import S3Client
from typing import Literal

__all__ = ("client_r2",)

client_r2 = boto3.client(
    service_name="s3",
    endpoint_url=cfSettings.R2_ENDPOINT,
    aws_access_key_id=cfSettings.ACCESS_KEY,
    aws_secret_access_key=cfSettings.SECRET_ACCESS_KEY,
    region_name=cfSettings.LOCATION,
)


from contextlib import AsyncExitStack

from aiobotocore.session import AioSession


class Manager:
    def __init__(self):
        self._exit_stack = AsyncExitStack()
        self._s3_client = None

    async def getHeadObjectR2(self, *, Bucket: str, Key: str):
        # Bucket=cfSettings.BUCKET, Key=key
        head_object = await self._s3_client.head_object(Bucket=Bucket, Key=Key)
        return head_object

    async def copyObjectR2(
        self,
        *,
        Bucket: str,
        Key: str,
        CopySource: str,
        MetadataDirective: Literal["COPY", "REPLACE"]
    ):
        # Bucket=cfSettings.BUCKET,
        # Key=new_key,
        # CopySource=f"{cfSettings.BUCKET}/{key}",
        copy_response = await self._s3_client.copy_object(
            Bucket=Bucket,
            Key=Key,
            CopySource=CopySource,
            MetadataDirective=MetadataDirective,
        )
        return copy_response

    async def deleteObjectR2(self, *, Bucket: str, Key: str):
        delete_response = await self._s3_client.delete_object(Bucket=Bucket, Key=Key)
        return delete_response

    async def __aenter__(self):
        session = AioSession()
        self._s3_client = await self._exit_stack.enter_async_context(
            session.create_client(
                "s3",
                endpoint_url=cfSettings.R2_ENDPOINT,
                aws_access_key_id=cfSettings.ACCESS_KEY,
                aws_secret_access_key=cfSettings.SECRET_ACCESS_KEY,
                region_name=cfSettings.LOCATION,
            )
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)


async def create_s3_client(session: AioSession, exit_stack: AsyncExitStack):
    # Create client and add cleanup
    client = await exit_stack.enter_async_context(
        session.create_client(
            "s3",
            endpoint_url=cfSettings.R2_ENDPOINT,
            aws_access_key_id=cfSettings.ACCESS_KEY,
            aws_secret_access_key=cfSettings.SECRET_ACCESS_KEY,
            region_name=cfSettings.LOCATION,
        )
    )
    return client


async def non_manager_example():
    session = AioSession()
    async with Manager() as S3_client:
        S3_client

    async with AsyncExitStack() as exit_stack:
        s3_client: S3Client = await create_s3_client(session, exit_stack)

        # do work with s3_client
