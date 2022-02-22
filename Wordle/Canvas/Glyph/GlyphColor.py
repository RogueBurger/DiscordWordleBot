from enum import Enum


class GlyphColor(Enum):
    GREEN = ('#6aaa64ff', '#6aaa64ff', '#ffffff00')
    YELLOW = ('#c9b458ff', '#c9b458ff', '#ffffff00')
    RED = ('#ff4646ff', '#ff4646ff', '#ffffff00')
    CLEAR = ('#00000000', '#00000000', '#00000000')

    DARK_GRAY = ('#454545ff', '#454545ff', '#ffffff00')
    INVERSE_DARK_GRAY = ('#ffffff00', '#454545ff', '#454545ff')

    GRAY = ('#565758ff', '#565758ff', '#ffffff00')
    INVERSE_GRAY = ('#ffffff00', '#565758ff', '#565758ff')

    LIGHT_GRAY = ('#86888aff', '#86888aff', '#ffffff00')
    INVERSE_LIGHT_GRAY = ('#ffffff00', '#86888aff', '#86888aff')

    def __str__(self) -> str:
        return self.name
