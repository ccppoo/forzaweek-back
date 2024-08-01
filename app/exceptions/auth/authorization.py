__all__ = ("NotAuthorized",)


class NotAuthorized(Exception):
    def __init__(self, details):
        super().__init__("Not Authorized")
