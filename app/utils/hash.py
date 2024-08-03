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


def _gen_uuid(*, value: str) -> str:

    uuid = str(uuid5(NAMESPACE_OID, value))

    return uuid


def gen_post_uuid(creator_oid: str, created_at: int) -> str:
    """_summary_

    Args:
        creator_oid (str): user model ObjectID
        created_at (int): post created UNIX timestamp(int)

    Returns:
        str: UUID
    """
    # 게시물 역추적, 무작위 대입 방지
    target = creator_oid + securitySettings.UID_GEN_SALT_PUBLIC + str(created_at)
    return _gen_uuid(target)
