from __future__ import annotations
import pathlib
import os
from app.configs import runtimeSettings, cfSettings
from typing import Tuple, Union
from app.types.http import Url
from app.cloud import client_r2
from pydantic import BaseModel
from .temp import (
    R2_object_head_response,
    R2_ObjectMetaData,
    R2_object_delete_response,
    R2_object_copy_response,
)
from app.utils.image import get_key, update_key, key_to_url
from pprint import pprint

# from mypy_boto3_s3.type_defs import CopyObjectOutputTypeDef

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import UserAuth


# FIXME: async 병렬 or 병렬
def resolve_temp_image(
    folder: str, temp_image: str, new_name: str, user: UserAuth, *paths: Tuple[str]
) -> Union[Url, None]:

    base_dir = runtimeSettings.TEMPFILE_BASE_DIR
    new_name_ = new_name.replace(" ", "_")

    fname_temp = pathlib.Path(base_dir, "uploads", folder, temp_image).resolve()

    if not fname_temp.exists():
        # TODO: 업로드된 이미지 다시 요청
        return None

    # 업로드할 이미지 이름 재수정
    new_filename = f"{new_name_}{fname_temp.suffix}"
    paths_ = [p.replace(" ", "_") for p in paths]
    resolved_key = "/".join([folder, *paths_, new_filename])

    CONTENT_TYPE = None
    if fname_temp.suffix.endswith("svg"):
        CONTENT_TYPE = "svg+xml"
    if fname_temp.suffix.endswith("webp"):
        CONTENT_TYPE = "webp"
    if fname_temp.suffix.endswith("png"):
        CONTENT_TYPE = "png"
    if fname_temp.suffix.endswith("jpg"):
        CONTENT_TYPE = "jpg"
    # https://fzwcdn.forzaweek.com/board/board/test/1eac1219-bb82-4c47-b88e-9b5cc757d3fd.jpg

    # TODO
    metadata = R2_ObjectMetaData(user_id=user.user_id, user_doc_id=str(user.id))
    """
    MetaData : 이미지 메타데이타에 업로드한 사용자 노출용 UID, Document ID 첨부해서
    삭제할 때 JWT로 1차 검증하고, 삭제할 때 
    """
    client_r2.upload_file(
        Filename=fname_temp,
        Bucket=cfSettings.BUCKET,
        Key=resolved_key,
        ExtraArgs={
            "ContentType": f"image/{CONTENT_TYPE}",
            "Metadata": metadata.model_dump(),
        },
    )

    # 임시 파일 삭제
    os.remove(fname_temp)

    # 업로드하고 Url 반환
    image_url = f"{cfSettings.URL_BASE}/{resolved_key}"
    return image_url


# FIXME: async 병렬 or 병렬
def delete_uploade_image(originImageURL: str, user: UserAuth) -> Union[Url, None]:
    # TODO: purge cache after deleting image
    # doc : https://developers.cloudflare.com/api/operations/zone-purge#purge-cached-content-by-url
    # default -> 4 hours
    uploaded_file_key = originImageURL.replace(cfSettings.URL_BASE, "")[1:]
    # NOTE: 그냥 R2 worker 만들어서 할까..?

    print()
    print(f"{originImageURL=}")
    print()
    print(f"{uploaded_file_key=}")
    print()

    head = client_r2.head_object(Bucket=cfSettings.BUCKET, Key=uploaded_file_key)
    # 여기서 업로드한 사용자 public user_id + document(private) user_id 검증해서 삭제하면 됨
    # 클플에 직접 따로 보내는 과정인 경우에 (이미지 처음 생성하는 경우, 메타 데이터가 없음)
    # 글 최초 작성시에 이미지 올릴 때 첨부할 수 있는 메타 태그는 JSON 토큰에서 추출할 수 있는 'koreajun797@naver.com'
    head_resposne = R2_object_head_response(**head)
    # should be
    match_user_email = (
        head_resposne.Metadata.upload_user_email == user.oauth.microsoft.email
    )
    user_oid = head_resposne.Metadata.upload_user_oid
    match_user_oid = True

    if user_oid:
        # 업로드 된 사진의 경우 (글 최초 작성중이 아닌)
        match_user_oid = user_oid == str(user.id)

    if match_user_email or (user_oid and match_user_oid):
        reply = client_r2.delete_object(Bucket=cfSettings.BUCKET, Key=uploaded_file_key)
        delete_response = R2_object_delete_response(**reply)

        pprint(delete_response)
    # 사용자 정보 일치하지 않는 경우 내가 알아서 처리해야함
    # delete_response.is_success (HTTP code 204 반환)

    return


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
