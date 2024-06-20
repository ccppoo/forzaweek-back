import pathlib
import os
from app.configs import runtimeSettings, cfSettings
from typing import Tuple, Union
from app.types.http import Url
from app.cloud import client_r2


# FIXME: async 병렬 or 병렬
def resolve_temp_image(
    folder: str, temp_image: str, new_name: str, *paths: Tuple[str]
) -> Union[Url, None]:

    base_dir = runtimeSettings.TEMPFILE_BASE_DIR

    fname_temp = pathlib.Path(base_dir, "uploads", folder, temp_image).resolve()

    if not fname_temp.exists():
        # TODO: 업로드된 이미지 다시 요청
        return None

    # 업로드할 이미지 이름 재수정
    new_filename = f"{new_name}{fname_temp.suffix}"
    resolved_key = "/".join([folder, *paths, new_filename])

    CONTENT_TYPE = None
    if fname_temp.suffix.endswith("svg"):
        CONTENT_TYPE = "svg+xml"
    if fname_temp.suffix.endswith("webp"):
        CONTENT_TYPE = "webp"
    if fname_temp.suffix.endswith("png"):
        CONTENT_TYPE = "png"

    client_r2.upload_file(
        Filename=fname_temp,
        Bucket=cfSettings.BUCKET,
        Key=resolved_key,
        ExtraArgs={"ContentType": f"image/{CONTENT_TYPE}"},
    )

    # 임시 파일 삭제
    os.remove(fname_temp)

    # 업로드하고 Url 반환
    image_url = f"{cfSettings.URL_BASE}/{resolved_key}"
    return image_url
