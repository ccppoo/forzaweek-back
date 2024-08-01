__all__ = ("InvalidAuthorizationToken",)


class InvalidAuthorizationToken(Exception):
    def __init__(self, details):
        super().__init__("Invalid authorization token: " + details)
