from __future__ import annotations
from app.configs import runtimeSettings, cfSettings
from typing import Tuple, Union
from app.types.http import Url
from app.cloud import client_r2, Manager
from pydantic import BaseModel

from app.schemas.cloudflare.r2 import (
    R2_object_head_response,
    R2_object_copy_response,
    R2_object_delete_response,
)
from app.schemas.cloudflare.object_meta import R2_ObjectMetaData
from app.utils.image import get_key, update_key, key_to_url
from pprint import pprint

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import UserAuth


def update_file_key(image_url: str, user: UserAuth) -> str:
    """
    upload/user/ ...  -> /board/post/ ... 으로 변환

    # 최초 작성의 경우 (CF worker가 토큰만으로 식별하기 때문에 email 밖에 없음)

    1. 이미지 올린 사람이 맞는지 HEAD response를 통해서 확인
    2. 기존 object를 자동 삭제가 안되는 key path로 복사
    3. 복사 성공하고, 원래 있던 TEMP 파일은 삭제

    # 수정의 경우 (upload/user/ ... 이 아닌 다른 이미지 파일의 경우)

    1. key가 임시 파일 PATH가 아닌 경우 pass (이거는 앞에서 먼저 걸러줌)
    """
    key = get_key(image_url)
    # print()
    # print(f"{key=}")
    # return
    # 1. 이미지 올린 사람이 맞는지 HEAD response를 통해서 확인
    # print(f"get head object : {key=}")
    head = client_r2.head_object(Bucket=cfSettings.BUCKET, Key=key)
    head_resposne = R2_object_head_response(**head)
    # should be
    match_user_email = (
        head_resposne.Metadata.upload_user_email == user.oauth.microsoft.email
    )

    if not match_user_email:
        return
    # print(f"{match_user_email=} {head_resposne.Metadata.upload_user_email}")
    # 2. 원래 있던 object 복사
    new_key = update_key("board/post", key.removeprefix("user/upload/"))
    # returns CopyObjectOutputTypeDef

    metadata = R2_ObjectMetaData(
        upload_user_email=user.oauth.microsoft.email, upload_user_oid=str(user.id)
    )
    print(f"board/post로 옮기는 이미지 새로운 메타 데이타")
    pprint(metadata)

    copy_response = client_r2.copy_object(
        Bucket=cfSettings.BUCKET,
        Key=new_key,
        CopySource=f"{cfSettings.BUCKET}/{key}",
        Metadata=metadata.model_dump(),
        MetadataDirective="REPLACE",
    )
    # print()
    # pprint(copy_response)
    # print()
    copy_response = R2_object_copy_response(**copy_response)

    # 3. 기존 object 삭제
    reply = client_r2.delete_object(Bucket=cfSettings.BUCKET, Key=key)
    delete_response = R2_object_delete_response(**reply)

    # pprint(delete_response)
    # print()
    # 4. 새로운 key url 반환
    new_key_url = key_to_url(new_key)
    # print(f"{new_key_url=}")
    # print()

    return new_key_url


async def promote_to_permanent(image_url: str, destination: str, user: UserAuth) -> str:
    """
    upload/user/ ...  -> /board/post/ ... 으로 변환

    # 최초 작성의 경우 (CF worker가 토큰만으로 식별하기 때문에 email 밖에 없음)

    1. 이미지 올린 사람이 맞는지 HEAD response를 통해서 확인
    2. 기존 object를 자동 삭제가 안되는 key path로 복사
    3. 복사 성공하고, 원래 있던 TEMP 파일은 삭제

    # 수정의 경우 (upload/user/ ... 이 아닌 다른 이미지 파일의 경우)

    1. key가 임시 파일 PATH가 아닌 경우 pass (이거는 앞에서 먼저 걸러줌)
    """
    key = get_key(image_url)
    # print()
    # print(f"{key=}")
    # return
    # 1. 이미지 올린 사람이 맞는지 HEAD response를 통해서 확인
    # print(f"get head object : {key=}")
    new_key_url = None
    async with Manager() as s3Manager:
        head = await s3Manager.getHeadObjectR2(Bucket=cfSettings.BUCKET, Key=key)
        pprint(head)
        head_response = R2_object_head_response(**head)
        # should be
        matches_user = (
            head_response.Metadata.email == user.oauth.microsoft.email
            and head_response.Metadata.sub == user.oauth.microsoft.uid
        )
        # user.oauth.microsoft.uid : AAAAAAAAAAAAAAAAAAAAACYXE1VWFvkuKw434_Jtjfw
        if not matches_user:
            # TODO: hanling
            return
        # print(f"{match_user_email=} {head_resposne.Metadata.upload_user_email}")
        # 2. 원래 있던 object 복사
        "FH5/decal"
        new_key = update_key(destination, key.removeprefix("user/upload/"))
        # returns CopyObjectOutputTypeDef
        metadata = R2_ObjectMetaData(
            email=user.oauth.microsoft.email, sub=user.oauth.microsoft.uid
        )
        print(f"board/post로 옮기는 이미지 새로운 메타 데이타")
        pprint(metadata)
        copy_reply = await s3Manager.copyObjectR2(
            Bucket=cfSettings.BUCKET,
            Key=new_key,
            CopySource=f"{cfSettings.BUCKET}/{key}",
            MetadataDirective="COPY",
        )

        print()
        pprint(copy_reply)
        print()
        copy_response = R2_object_copy_response(**copy_reply)

        # 3. 기존 object 삭제
        delete_reply = await s3Manager.deleteObjectR2(Bucket=cfSettings.BUCKET, Key=key)
        delete_response = R2_object_delete_response(**delete_reply)
        pprint(delete_response)
        print()
        # 4. 새로운 key url 반환
        new_key_url = key_to_url(new_key)
        print(f"{new_key_url=}")
        print()

    return new_key_url


def update_to_permanent2(image_url: str, destination: str, user: UserAuth) -> str:
    """
    upload/user/ ...  -> /board/post/ ... 으로 변환

    # 최초 작성의 경우 (CF worker가 토큰만으로 식별하기 때문에 email 밖에 없음)

    1. 이미지 올린 사람이 맞는지 HEAD response를 통해서 확인
    2. 기존 object를 자동 삭제가 안되는 key path로 복사
    3. 복사 성공하고, 원래 있던 TEMP 파일은 삭제

    # 수정의 경우 (upload/user/ ... 이 아닌 다른 이미지 파일의 경우)

    1. key가 임시 파일 PATH가 아닌 경우 pass (이거는 앞에서 먼저 걸러줌)
    """
    key = get_key(image_url)
    # print()
    # print(f"{key=}")
    # return
    # 1. 이미지 올린 사람이 맞는지 HEAD response를 통해서 확인
    # print(f"get head object : {key=}")
    head = client_r2.head_object(Bucket=cfSettings.BUCKET, Key=key)
    head_response = R2_object_head_response(**head)
    # should be
    matches_user = (
        head_response.Metadata.uploaderEmail == user.oauth.microsoft.email
        and head_response.Metadata.sub == user.oauth.microsoft.uid
    )
    # user.oauth.microsoft.uid : AAAAAAAAAAAAAAAAAAAAACYXE1VWFvkuKw434_Jtjfw

    if not matches_user:
        # TODO: hanling
        return
    # print(f"{match_user_email=} {head_resposne.Metadata.upload_user_email}")
    # 2. 원래 있던 object 복사
    "FH5/decal"
    new_key = update_key(destination, key.removeprefix("user/upload/"))
    # returns CopyObjectOutputTypeDef

    metadata = R2_ObjectMetaData(
        uploaderEmail=user.oauth.microsoft.email, sub=user.oauth.microsoft.uid
    )
    print(f"board/post로 옮기는 이미지 새로운 메타 데이타")
    pprint(metadata)

    copy_response = client_r2.copy_object(
        Bucket=cfSettings.BUCKET,
        Key=new_key,
        CopySource=f"{cfSettings.BUCKET}/{key}",
        # Metadata=metadata.model_dump(),
        MetadataDirective="",
    )
    print()
    pprint(copy_response)
    print()
    copy_response = R2_object_copy_response(**copy_response)

    # 3. 기존 object 삭제
    reply = client_r2.delete_object(Bucket=cfSettings.BUCKET, Key=key)
    delete_response = R2_object_delete_response(**reply)

    pprint(delete_response)
    print()
    # 4. 새로운 key url 반환
    new_key_url = key_to_url(new_key)
    print(f"{new_key_url=}")
    print()

    return new_key_url
