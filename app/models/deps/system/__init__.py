from .image import HasMultipleImages, HasSingleImage
from .uploader import HasUploader
from .game import GameBase


class PostWithImage(HasUploader, HasMultipleImages):
    pass
