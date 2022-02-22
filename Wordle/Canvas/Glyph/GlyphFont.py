from os.path import basename

from PIL import ImageFont


class GlyphFont(ImageFont.FreeTypeFont):
    def __init__(self, font_path: str, size: int):
        super().__init__(font=font_path, size=size)

    def __str__(self) -> str:
        return '::'.join([
            basename(self.path),
            str(self.size)
        ])
