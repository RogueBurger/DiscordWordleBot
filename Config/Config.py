from pathlib import Path
from pydantic import BaseModel, validator
from typing import Union

from Config.Base import Settings


class GlyphConfig(BaseModel):
    font_path: str = './Assets/Fonts/static/SourceCodePro-SemiBold.ttf'

    # Determines default size of Glyph (maps to GlyphSize enum)
    default_size: str = 'SMALL'

    # Determines the space between embedded character and edge of glyph image
    horizontal_pad_factor: float = 2.0
    vertical_pad_factor: float = 0.7

    # Determines whether to coerce the glyph image into a square
    square: bool = True

    # Determines the width of the border as a % of glyph image width
    border_width_factor: float = 0.06

    # Determines y-offset of character embedded in glyph image
    vertical_offset_factor: float = 1.31

    @validator('font_path')
    def font_path_exists(cls, v):
        if Path(v).exists():
            return v
        raise ValueError('file not found')

    @validator('default_size')
    def default_size_is_valid(cls, v):
        valid = ['SMALL', 'MEDIUM', 'LARGE']
        res = str(v).upper()
        if res in valid:
            return res
        raise ValueError(
            f'value is not a valid log level permitted: {", ".join(valid)}')


class CanvasConfig(BaseModel):
    glyph: GlyphConfig = GlyphConfig()


class RedisConfig(BaseModel):
    enable: bool = False
    host: str = '127.0.0.1'
    port: Union[str, int] = 6379

    @validator('host', 'port', each_item=True)
    def host_port_not_empty_if_enabled(cls, v, values):
        if 'enable' in values and not v:
            raise ValueError('cannot be empty when redis enabled')
        return v

    @validator('port')
    def port_is_int(cls, v):
        try:
            return int(v)
        except ValueError:
            raise ValueError('must be an integer')


class Config(Settings):
    token: str
    wordlist: str

    log_level: str = 'INFO'
    verbose: bool = False

    redis: RedisConfig = RedisConfig()
    canvas: CanvasConfig = CanvasConfig()

    allow_channels: list[int] = []
    deny_channels: list[int] = []

    @validator('log_level')
    def log_level_supported(cls, v):
        valid = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL', 'FATAL']
        res = str(v).upper()
        if res in valid:
            return res
        raise ValueError(
            f'value is not a valid log level; permitted: {", ".join(valid)}')
