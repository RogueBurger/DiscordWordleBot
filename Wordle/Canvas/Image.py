import uuid

from io import BytesIO

from discord import File

from PIL import Image as PILImage


class Image():
    def __init__(self, image: PILImage, format: str = 'png'):
        self.id: str = str(uuid.uuid4())
        self.image: PILImage = image
        # self.border_width: int = border_width
        self.format: str = format

    def __str__(self):
        return '.'.join([self.id, self.format])

    @property
    def name(self) -> str:
        return '.'.join([self.id, self.format])

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height

    def to_discord_file(self) -> File:
        arr = BytesIO()
        self.image.save(arr, format=self.format)
        arr.seek(0)
        return File(arr, self.name)
