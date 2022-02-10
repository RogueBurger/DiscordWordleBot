from dataclasses import dataclass
from typing import Tuple

from .GlyphSize import GlyphSize
from .GlyphFont import GlyphFont


@dataclass
class GlyphTemplate:
    font: GlyphFont
    width: float
    height: float
    vertical_offset: int

    def __init__(self,
                 font_path: str,
                 font_size: GlyphSize,
                 alphabet: str,
                 horizontal_pad_factor: float,
                 vertical_pad_factor: float,
                 vertical_offset_factor: float,
                 square: bool):

        font = GlyphFont(font_path=font_path, size=font_size)

        char_sizes = [font.getsize(char) for char in alphabet]
        char_heights = [x[1] for x in char_sizes]

        max_char_width = max([x[0] for x in char_sizes])
        max_char_height = max(char_heights)
        mode_char_height = max(char_heights, key=char_heights.count)

        glyph_width = max_char_width + \
            int(max_char_width * horizontal_pad_factor)
        glyph_height = max_char_height + \
            int(max_char_height * vertical_pad_factor)

        self.font = font
        self.alphabet = alphabet
        self.width = max(glyph_width, glyph_height) if square else glyph_width
        self.height = max(
            glyph_width, glyph_height) if square else glyph_height

        self.vertical_offset = (
            int(self.height - mode_char_height * vertical_offset_factor) / 2)

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    @property
    def coords(self) -> Tuple[int, int, int, int]:
        return 0, 0, self.width, self.height

    def char_anchor_coords(self, char: str) -> Tuple[int, int]:
        char_width, _ = self.font.getsize(char)
        return int((self.width - char_width) / 2), self.vertical_offset
