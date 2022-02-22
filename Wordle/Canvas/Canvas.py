
import logging
import math

from typing import List, Tuple

from PIL import Image as PILImage

from Config import CanvasConfig

from Wordle.Canvas.Glyph import (
    Glyph, GlyphCollection, GlyphColor, GlyphShape,
    GlyphFactory, GlyphNotFound)
from Wordle.Canvas.Image import Image


class Canvas:
    def __init__(self, config: CanvasConfig):
        self._glyphs: GlyphCollection = GlyphCollection()
        self._glyph_factory: GlyphFactory = GlyphFactory(config.glyph)

        self.spacer_width = config.glyph.spacer_width

    def draw_char(
            self,
            char: str,
            shape: GlyphShape,
            color: GlyphColor) -> Glyph:

        try:
            return self._glyphs.get(name=char, shape=shape, color=color)
        except GlyphNotFound:
            ...

        glyph = self._glyph_factory.create_glyph(
            char=char, shape=shape, color=color)
        self._glyphs.add(glyph)

        logging.getLogger('WordleBot.Canvas').debug(
            f'Added {glyph} to the collection')

        return glyph

    def draw_word(
            self,
            word: List[Tuple[str, GlyphColor]],
            shape: GlyphShape = GlyphShape.DEFAULT) -> Image:

        if word is None:
            return Image(image=PILImage.new('RGBA', (0, 0)))

        cols = len(word)

        glyphs = [
            self.draw_char(
                char=char[0], shape=shape, color=char[1])
            for char in word if char]

        word_width = sum([glyph.width for glyph in glyphs[0:cols]])
        img_width = word_width + (cols * self.spacer_width) + self.spacer_width

        word_height = max([glyph.height for glyph in glyphs])
        img_height = word_height + 2 * self.spacer_width

        img = PILImage.new('RGBA', (img_width, img_height))

        for idx, glyph in enumerate(glyphs):
            x_off = self.spacer_width + \
                (idx % cols) * (glyph.width + self.spacer_width)
            img.paste(glyph.image, (x_off, self.spacer_width))

        return Image(image=img)

    def vertical_join(self, images: List[Image]) -> Image:
        if len(images) == 1:
            return images[0]

        width = max([im.width for im in images])
        height = sum(
            [im.height - self.spacer_width for im in images]) + self.spacer_width

        res = PILImage.new('RGBA', (width, height))

        y_offset = 0
        for im in images:
            x_offset = max(0, math.ceil((width - im.width) / 2))
            res.paste(im.image, (x_offset, y_offset))
            y_offset = y_offset + im.height - self.spacer_width

        return Image(res)
