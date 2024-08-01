from uuid import uuid5, NAMESPACE_OID
from app.configs import securitySettings


def user_uuid() -> str:
    # 사용자 고유 ID + salt 추가해서 역으로 대입하지 못하도록
    uuid = str(uuid5(NAMESPACE_OID, securitySettings.UID_GEN_SALT))

    return uuid


def gen_user_uuid(*, uid: str, email: str) -> str:
    # 사용자 고유 ID + salt 추가해서 역으로 대입하지 못하도록
    uuid = str(uuid5(NAMESPACE_OID, email + securitySettings.UID_GEN_SALT + uid))

    return uuid
