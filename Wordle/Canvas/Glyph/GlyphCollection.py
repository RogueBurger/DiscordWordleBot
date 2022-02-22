from typing import Dict, Optional

from .GlyphError import GlyphNotFound
from .Glyph import Glyph
from .GlyphShape import GlyphShape
from .GlyphColor import GlyphColor


class GlyphCollection:
    _state: Dict[str, Glyph] = {}

    def key(self, name: str, shape: GlyphShape, color: GlyphColor) -> str:
        return Glyph.generate_id(name=name, shape=shape, color=color)

    def get(self, name: str, shape: GlyphShape, color: GlyphColor) -> Optional[Glyph]:
        try:
            return self._state[self.key(name=name, shape=shape, color=color)]
        except KeyError:
            raise GlyphNotFound()

    def add(self, glyph: Glyph, overwrite: bool = True) -> bool:
        key = self.key(name=glyph.name, shape=glyph.shape, color=glyph.color)

        if not overwrite and key in self._state:
            return False

        self._state[key] = glyph
        return True
