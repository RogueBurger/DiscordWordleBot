
import logging
import math

from typing import List, Optional, Tuple

from PIL import Image as PILImage, ImageOps

from Config import CanvasConfig

from Wordle.Canvas.Glyph import (
    Glyph, GlyphCollection, GlyphColor,
    GlyphFactory, GlyphNotFound, GlyphSize)
from Wordle.Canvas.Image import Image


class Canvas:
    def __init__(self, config: CanvasConfig):
        self._glyphs: GlyphCollection = GlyphCollection()
        self._glyph_factory: GlyphFactory = GlyphFactory(config.glyph)

        self.default_glyph_size: GlyphSize = GlyphSize[config.glyph.default_size]
        self.border_width_factor: float = config.glyph.border_width_factor

    def draw_char(
            self,
            char: str,
            size: GlyphSize = GlyphSize.LARGE,
            color: GlyphColor = GlyphColor.LIGHT_GRAY,
            rounded: bool = False) -> Glyph:

        try:
            return self._glyphs.get(name=char, size=size, color=color, rounded=rounded)
        except GlyphNotFound:
            ...

        glyph = self._glyph_factory.create_glyph(
            char=char, size=size, color=color, rounded=rounded)
        self._glyphs.add(glyph)

        logging.getLogger('WordleBot.Canvas').debug(
            f'Added {glyph} to the collection')

        return glyph

    def draw_word(
            self,
            word: List[Tuple[str, GlyphColor]],
            size: Optional[GlyphSize] = None,
            rounded: bool = False) -> Image:

        if word is None:
            return Image(image=PILImage.new('RGBA', (0, 0)), border_width=0)

        if size is None:
            size = self.default_glyph_size

        cols = len(word)

        glyphs = [
            self.draw_char(
                char=char[0], size=size,
                color=char[1], rounded=rounded)
            for char in word if char]

        border_width = int(
            max([glyph.width for glyph in glyphs[0:cols]]) * self.border_width_factor)

        word_width = sum([glyph.width for glyph in glyphs[0:cols]])
        img_width = word_width + (cols * border_width) + border_width

        word_height = max([glyph.height for glyph in glyphs])
        img_height = (word_height + border_width) + border_width

        img = PILImage.new('RGBA', (img_width, img_height))

        for idx, glyph in enumerate(glyphs):
            x_off = (idx % cols) * (glyph.width + border_width)
            img.paste(ImageOps.expand(
                glyph.image,
                border=border_width),
                (x_off, 0))

        return Image(image=img, border_width=border_width)

    def vertical_join(self, images: List[Image]) -> Image:
        if not images:
            return Image(image=PILImage.new('RGBA', (0, 0)), border_width=0)

        if len(images) == 1:
            return images[0]

        border_width = max([image.border_width for image in images])
        width = max([im.width for im in images])
        height = sum(
            [im.height - im.border_width for im in images]) + border_width

        res = PILImage.new('RGBA', (width, height))

        y_offset = 0
        for im in images:
            x_offset = max(0, math.ceil((width - im.width) / 2))
            res.paste(im.image, (x_offset, y_offset))
            y_offset = y_offset + im.height - im.border_width

        return Image(res, border_width=border_width)
