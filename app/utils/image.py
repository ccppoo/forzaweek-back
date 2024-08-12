from app.configs import cfSettings


def get_key(image_url: str) -> str:

    _key = image_url.removeprefix(cfSettings.URL_BASE)
    return _key.strip("/")


def update_key(prefix: str, key: str) -> str:
    new_key = "/".join([prefix, key.strip("/")])
    return new_key


def key_to_url(key: str) -> str:
    return f"{cfSettings.URL_BASE}/{key}"
