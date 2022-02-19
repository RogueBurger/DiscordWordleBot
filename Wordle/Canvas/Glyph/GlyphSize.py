from enum import IntEnum


class GlyphSize(IntEnum):
    SMALL: int = 30
    MEDIUM: int = 60
    LARGE: int = 90

    def __str__(self) -> str:
        return self.name
