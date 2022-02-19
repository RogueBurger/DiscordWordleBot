from typing import Dict, Optional

from .GlyphError import GlyphNotFound
from .Glyph import Glyph
from .GlyphSize import GlyphSize
from .GlyphColor import GlyphColor


class GlyphCollection:
    _state: Dict[str, Glyph] = {}

    def key(self, name: str, size: GlyphSize, color: GlyphColor, rounded: bool) -> str:
        return Glyph.generate_id(name=name, size=size, color=color, rounded=rounded)

    def get(self, name: str, size: GlyphSize, color: GlyphColor, rounded: bool) -> Optional[Glyph]:
        try:
            return self._state[self.key(name=name, size=size, color=color, rounded=rounded)]
        except KeyError:
            raise GlyphNotFound()

    def add(self, glyph: Glyph, overwrite: bool = True) -> bool:
        key = self.key(name=glyph.name, size=glyph.size,
                       color=glyph.color, rounded=glyph.rounded)

        if not overwrite and key in self._state:
            return False

        self._state[key] = glyph
        return True
