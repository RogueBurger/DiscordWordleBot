from dataclasses import dataclass
import math
from typing import Tuple

from .GlyphFont import GlyphFont


@dataclass
class GlyphTemplate:
    font: GlyphFont
    width: float
    height: float
    vertical_offset: int

    def __init__(self,
                 font_path: str,
                 font_size: int,
                 alphabet: str,
                 horizontal_pad: int,
                 vertical_pad: int,
                 border_width: int,
                 square: bool):

        font = GlyphFont(font_path=font_path, size=font_size)

        bbox_sizes = [font.getbbox(char) for char in alphabet]
        x1 = min([bbox[0] for bbox in bbox_sizes])
        y1 = min([bbox[1] for bbox in bbox_sizes])
        x2 = max([bbox[2] for bbox in bbox_sizes])
        y2 = max([bbox[3] for bbox in bbox_sizes])

        char_width = x2 - x1
        glyph_width = char_width + 2 * (horizontal_pad + border_width)
        glyph_width = math.ceil(glyph_width / 2) * 2

        char_height = y2 - y1
        glyph_height = char_height + 2 * (vertical_pad + border_width)
        glyph_height = math.ceil(glyph_height / 2) * 2

        char_heights = [bbox[3] - bbox[1] for bbox in bbox_sizes]
        mode_char_height = max(char_heights, key=char_heights.count)

        self.font = font
        self.alphabet = alphabet
        self.width = max(glyph_width, glyph_height) if square else glyph_width
        self.height = max(
            glyph_width, glyph_height) if square else glyph_height

        self.border_width = border_width
        self.vertical_offset = int((self.height - mode_char_height) / 2)

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    @property
    def coords(self) -> Tuple[int, int, int, int]:
        x1 = self.width - math.ceil(self.border_width / 2)
        y1 = self.height - math.ceil(self.border_width / 2)
        return 0, 0, self.width - 1, self.height - 1

    def char_anchor_coords(self, char: str) -> Tuple[int, int]:
        char_width, _ = self.font.getsize(char)
        return int((self.width - char_width) / 2), self.vertical_offset
