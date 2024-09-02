class RecursiveFetchException(Exception):
    def __init__(self, msg="Recursive Link Fetch called", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
