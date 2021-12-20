import io
import uuid

from enum import Enum
from typing import List

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
from discord import File


class UnsupportedCharacterException(Exception):
    pass


class UnsupportedColorException(Exception):
    pass


class Image:
    def __init__(self, image: PILImage, format = 'png'):
        self.id = str(uuid.uuid4())
        self.image = image
        self.format = format
        self.width = self.image.width
        self.height = self.image.height

    def name(self):
        return '.'.join([self.id, self.format])

    def to_discord_file(self) -> File:
        arr = io.BytesIO()
        self.image.save(arr, format=self.format)
        arr.seek(0)
        return File(arr, self.name())


class Glyph(Image):
    pass


class GlyphColor(Enum):
    HOT = ('#6aaa64ff', '#ffffffff')
    WARM = ('#c9b458ff', '#ffffffe6')
    COLD = ('#86888aff', '#ffffffcc')


class Canvas:
    # TODO: Implement a safe solution for a dynamic alphabet
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ-'
    COLORS = [x for x in GlyphColor]
    BGCOLOR = '#ffffff'

    FONT_PATH = './Assets/Fonts/static/SourceCodePro-SemiBold.ttf'
    FONT_SIZE = 30
    FONT_WIDTH_OFFSET_FACTOR = 1
    FONT_HEIGHT_OFFSET_FACTOR = 1.31
    HORIZONTAL_PADDING_FACTOR = 0.7
    VERTICAL_PADDING_FACTOR = 0.2

    def __init__(self):
        self._font = ImageFont.truetype(self.FONT_PATH, self.FONT_SIZE)
        self._glyphs = {
            char: {
                color: None for color in self.COLORS
            } for char in list(self.ALPHABET)
        }

        char_sizes = [self._font.getsize(char) for char in self.ALPHABET]
        char_widths = [x[0] for x in char_sizes]
        char_heights = [x[1] for x in char_sizes]
        max_char_width = max(char_widths)
        max_char_height = max(char_heights)
        mode_char_height = max(char_heights, key=char_heights.count)

        self.glyph_width = max_char_width + int(max_char_width * self.HORIZONTAL_PADDING_FACTOR)
        self.glyph_height = max_char_height + int(max_char_height * self.VERTICAL_PADDING_FACTOR)
        self.vertical_offset = (self.glyph_height - int(mode_char_height * self.FONT_HEIGHT_OFFSET_FACTOR)) / 2

    def draw_char(self, char: str, color: GlyphColor) -> Glyph:
        if char not in self._glyphs.keys():
            raise UnsupportedCharacterException

        if color not in self.COLORS or color not in self._glyphs[char].keys():
            raise UnsupportedColorException

        if not self._glyphs[char][color]:
            self._generate_glyph(char=char, color=color)

        return self._glyphs[char][color]

    def _generate_glyph(self, char: str, color: GlyphColor):
        img = PILImage.new(
            'RGBA',
            (self.glyph_width, self.glyph_height),
            color=color.value[0])

        draw = ImageDraw.Draw(img)

        width, height = draw.textsize(char, font=self._font)
        width = int(width * self.FONT_WIDTH_OFFSET_FACTOR)
        height = int(height * self.FONT_HEIGHT_OFFSET_FACTOR)

        draw.text(
            ((self.glyph_width - width) / 2, self.vertical_offset),
            text=char,
            font=self._font,
            fill=color.value[1])

        self._glyphs[char][color] = Glyph(image=img)

    def draw_word(self, glyphs: List[Glyph]) -> Image:
        img = PILImage.new(
            'RGBA',
            (self.glyph_width * len(glyphs), self.glyph_height),
            color=self.BGCOLOR)

        for idx, glyph in enumerate(glyphs):
            img.paste(glyph.image, (idx * self.glyph_width, 0))

        return Image(img)

    def vertical_join(self, top: Image, bottom: Image) -> Image:
        img = PILImage.new(
            'RGBA',
            (max(top.width, bottom.width), top.height + bottom.height),
            color=self.BGCOLOR)

        img.paste(top.image, (0, 0))
        img.paste(bottom.image, (0, top.height))

        return Image(img)
