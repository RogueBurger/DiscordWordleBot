from dataclasses import dataclass

from Wordle.Canvas.Image import Image

from .GlyphColor import GlyphColor
from .GlyphFont import GlyphFont
from .GlyphShape import GlyphShape


@dataclass
class Glyph:
    name: str
    image: Image
    font: GlyphFont
    shape: GlyphShape
    color: GlyphColor

    def __repr__(self) -> str:
        id = Glyph.generate_id(name=self.name, shape=self.shape,
                               color=self.color)
        return f'<{self.__class__.__name__} {id}>'

    @staticmethod
    def generate_id(name: str, shape: GlyphShape, color: GlyphColor) -> str:
        return '::'.join([str(x) for x in [name, shape, color]])

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height

    @property
    def border_width(self) -> int:
        return self.image.border_width
