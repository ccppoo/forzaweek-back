from uuid import uuid4


def random_uuid(*, replace_dash: str = None) -> str:
    uuid = str(uuid4())
    if replace_dash is None:
        return uuid
    return uuid.replace("-", replace_dash)
