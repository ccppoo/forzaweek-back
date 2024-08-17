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
