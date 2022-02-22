from enum import Enum, auto


class GlyphShape(Enum):
    DEFAULT = auto()
    WIDE = auto()

    def __str__(self) -> str:
        return self.name
