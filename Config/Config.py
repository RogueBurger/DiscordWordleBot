
from dataclasses import dataclass, is_dataclass, Field
from distutils.util import strtobool
from typing import Any, Dict, Optional

from dynaconf import LazySettings, Validator, ValidationError


class ConfigValidationError(Exception):
    ...


@dataclass
class RedisConfig():
    enable: bool
    host: str
    port: int


@dataclass
class Config():
    token: str
    wordlist: str
    log_level: str
    allow_channels: list[int]
    deny_channels: list[int]
    redis: RedisConfig

    def __init__(self,
                 load_dotenv: bool = True,
                 envvar_prefix: str = 'WORDLEBOT',
                 settings_files: list[str] = ['config.yaml'],
                 yaml_loader: str = 'safe_load'):

        log_levels = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']

        config = LazySettings(
            load_dotenv=load_dotenv,
            envvar_prefix=envvar_prefix,
            settings_files=settings_files,
            yaml_loader=yaml_loader,
            validators=[
                Validator('token', 'wordlist', required=True),
                Validator(
                    'log_level',
                    default='INFO',
                    condition=lambda x: x.upper() in log_levels,
                    messages={
                        'condition': ' '.join([
                            'Invalid {name} "{value}", must be one of: ',
                            ', '.join(log_levels)
                        ])
                    }),
                Validator('allow_channels', 'deny_channels', default=[]),
                Validator('redis.enable', default=False),
                Validator('redis.host', default='127.0.0.1'),
                Validator('redis.port', default=6379),
                Validator('redis.host', 'redis.port',
                          when=Validator('redis.enable', eq=True),
                          condition=lambda x: x,
                          messages={
                              'condition': 'host and port cannot be empty'
                          })
            ])

        try:
            config.validators
        except ValidationError as e:
            raise ConfigValidationError(e)

        config.log_level = config.log_level.upper()

        for attr, val in self._lazysettings_attr_mapper(config).items():
            self.__setattr__(attr, val)

    def _lazysettings_attr_mapper(
            self,
            settings: LazySettings,
            fields: Optional[Dict[str, Field]] = None,
            prefix: Optional[str] = None) -> Dict[str, Any]:

        res = {}

        fields = fields or self.__dataclass_fields__
        for _, field in fields.items():
            if is_dataclass(field.type):
                res[field.name] = field.type(
                    **self._lazysettings_attr_mapper(
                        settings=settings,
                        fields=field.type.__dataclass_fields__,
                        prefix=field.name))
                continue

            key = '.'.join(filter(None, [prefix, field.name]))

            val = settings.get(key)
            if field.type == bool and not isinstance(val, bool):
                val = strtobool(str(val))

            res[field.name] = val

        return res
