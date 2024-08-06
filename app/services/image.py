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
    # ACL, CacheControl, ChecksumAlgorithm, ContentDisposition, ContentEncoding,
    # ContentLanguage, ContentType, ExpectedBucketOwner, Expires,
    # GrantFullControl, GrantRead, GrantReadACP, GrantWriteACP, Metadata,
    # ObjectLockLegalHoldStatus, ObjectLockMode, ObjectLockRetainUntilDate,
    # RequestPayer, ServerSideEncryption, StorageClass, SSECustomerAlgorithm,
    # SSECustomerKey, SSECustomerKeyMD5, SSEKMSKeyId, SSEKMSEncryptionContext, Tagging, WebsiteRedirectLocation

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
            "Metadata": {
                "upload_user_id": "123",
                "upload_user_doc_id": "aaabbbccc",
            },
        },
    )

    # 임시 파일 삭제
    os.remove(fname_temp)

    # 업로드하고 Url 반환
    image_url = f"{cfSettings.URL_BASE}/{resolved_key}"
    return image_url


# FIXME: async 병렬 or 병렬
def delete_uploade_image(originImageURL: str) -> Union[Url, None]:

    uploaded_file_key = originImageURL.replace(cfSettings.URL_BASE, "")[1:]
    # NOTE: 그냥 R2 worker 만들어서 할까..?
    # client_r2.download_file
    # attr = client_r2.get_object_attributes(
    #     Bucket=cfSettings.BUCKET, Key=uploaded_file_key, ObjectAttributes=["ETag"]
    # )
    print()

    print(f"{originImageURL=}")
    print()
    print(f"{uploaded_file_key=}")
    print()
    from pprint import pprint

    head = client_r2.head_object(Bucket=cfSettings.BUCKET, Key=uploaded_file_key)
    head[
        "Metadata"
    ]  # 여기서 업로드한 사용자 public user_id + document(private) user_id 검증해서 삭제하면 됨
    pprint(head)

    # client_r2.delete_object(Bucket=cfSettings.BUCKET, Key=uploaded_file_key)

    return
