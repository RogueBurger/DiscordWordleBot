import string
from typing import Dict

from PIL import ImageDraw, ImageColor
from PIL import Image as PILImage

from Config import GlyphConfig

from .Glyph import Glyph
from .GlyphColor import GlyphColor
from .GlyphSize import GlyphSize
from .GlyphTemplate import GlyphTemplate


class GlyphFactory:
    def __init__(self, config: GlyphConfig):
        self._alphabet: str = ' ' + ''.join([string.printable.replace(char, '')
                                             for char in string.whitespace])
        self._error_char = '?'
        self._error_color = GlyphColor.RED

        assert self._error_char in self._alphabet

        self._templates: Dict[GlyphSize, GlyphTemplate] = {
            font_size.name: GlyphTemplate(
                alphabet=self._alphabet,
                font_path=config.font_path,
                font_size=font_size,
                horizontal_pad_factor=config.horizontal_pad_factor,
                vertical_pad_factor=config.vertical_pad_factor,
                vertical_offset_factor=config.vertical_offset_factor,
                square=config.square
            ) for font_size in GlyphSize
        }

    def create_glyph(self,
                     char: str,
                     size: GlyphSize,
                     color: GlyphColor,
                     rounded: bool = False) -> Glyph:

        tpl = self._templates[size.name]

        if char not in self._alphabet:
            char = self._error_char
            color = self._error_color

        radius = tpl.size[0] / 4 if rounded else 0
        outline_width = int(tpl.size[0] / 25) if rounded else 0

        background_color = (0, 0, 0, 0)
        font_color = (255, 255, 255, 255)
        fill_color = ImageColor.getcolor(color.value, 'RGBA')
        outline_color = tuple(fill_color[0:3]) + tuple([204])

        img = PILImage.new('RGBA', tpl.size, color=background_color)
        draw = ImageDraw.Draw(img, 'RGBA')

        draw.rounded_rectangle(
            tpl.coords,
            radius=radius,
            fill=fill_color,
            width=outline_width,
            outline=outline_color)

        draw.text(
            tpl.char_anchor_coords(char=char),
            text=char,
            font=tpl.font,
            fill=font_color)

        return Glyph(name=char, image=img, font=tpl.font,
                     size=size, color=color, rounded=rounded)
