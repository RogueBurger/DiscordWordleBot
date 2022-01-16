from dataclasses import dataclass

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
                 settings_files: list[str] = ['config.yaml']):

        config = LazySettings(
            load_dotenv=load_dotenv,
            envvar_prefix=envvar_prefix,
            settings_files=settings_files,
            validators=[
                Validator('token', 'wordlist', required=True),
                Validator('log_level', default='INFO', condition=lambda x: x in [
                          'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']),
                Validator('allow_channels', default=[]),
                Validator('deny_channels', default=[]),
                Validator('redis.enable', default=False),
                Validator('redis.port', default=6379),
                Validator('redis.host', 'redis.port',
                          required=True,
                          when=Validator('redis.enable', eq=True),
                          messages={'must_exist_true': '{name} is required when redis is enabled'})
            ])

        try:
            config.validators
        except ValidationError as e:
            raise ConfigValidationError(e)

        for field in self.__dataclass_fields__.keys():
            self.__setattr__(field, config.get(field))
