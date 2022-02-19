from dataclasses import dataclass

from Wordle.Canvas.Image import Image

from .GlyphColor import GlyphColor
from .GlyphFont import GlyphFont
from .GlyphSize import GlyphSize


@dataclass
class Glyph:
    name: str
    image: Image
    font: GlyphFont
    size: GlyphSize
    color: GlyphColor
    rounded: bool

    def __repr__(self) -> str:
        id = Glyph.generate_id(name=self.name, size=self.size,
                               color=self.color, rounded=self.rounded)
        return f'<{self.__class__.__name__} {id}>'

    @staticmethod
    def generate_id(name: str, size: GlyphSize, color: GlyphColor, rounded: bool) -> str:
        rounded_desc = 'ROUNDED' if rounded else 'UNROUNDED'
        return '::'.join([str(x) for x in [name, size, color, rounded_desc]])

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height

    @property
    def border_width(self) -> int:
        return self.image.border_width
