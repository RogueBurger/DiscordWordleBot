from enum import Enum


class GlyphColor(Enum):
    GREEN: str = '#538d4e'
    YELLOW: str = '#b59f3b'
    DARK_GRAY: str = '#454545'
    GRAY: str = '#565758'
    LIGHT_GRAY: str = '#969696'
    RED: str = '#ff4646'

    def __str__(self) -> str:
        return self.name
