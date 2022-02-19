from pathlib import Path
from pydantic import BaseModel, validator
from typing import Union

from Config.Base import Settings


class GlyphConfig(BaseModel):
    font_path: str = './Assets/Fonts/static/SourceCodePro-SemiBold.ttf'
    font_size: int = 60

    horizontal_pad: int = 6
    vertical_pad: int = 0
    spacer_width: int = 4
    border_width: int = 2

    # Determines whether to coerce the glyph image into a square
    square: bool = False

    wide_horizontal_pad: int = 35
    wide_vertical_pad: int = 0

    @validator('font_path')
    def font_path_exists(cls, v):
        if Path(v).exists():
            return v
        raise ValueError('file not found')


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
