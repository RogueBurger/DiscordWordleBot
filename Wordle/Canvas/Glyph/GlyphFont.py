from os.path import basename

from PIL import ImageFont

from .GlyphSize import GlyphSize


class GlyphFont(ImageFont.FreeTypeFont):
    def __init__(self, font_path: str, size: GlyphSize):
        super().__init__(font=font_path, size=size.value)

    def __str__(self) -> str:
        return '::'.join([
            basename(self.path),
            str(self.size)
        ])
