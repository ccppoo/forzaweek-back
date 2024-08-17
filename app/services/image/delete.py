from __future__ import annotations
import pathlib
import os
from app.configs import runtimeSettings, cfSettings
from typing import Tuple, Union
from app.types.http import Url
from app.cloud import client_r2
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
