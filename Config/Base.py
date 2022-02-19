import logging
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable
from typing import Dict, Any, Tuple
import yaml
from pathlib import Path


def yaml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    path = Path('config.yaml')
    encoding = settings.__config__.env_file_encoding

    try:
        with open(path, 'r', encoding=encoding) as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        logging.warn(
            f'No config file found at {path}')
        return {}


class Settings(BaseSettings):
    class Config:
        env_prefix = 'WORDLEBOT_'
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
        case_sensitive = False

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable
        ) -> Tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                env_settings,
                yaml_config_settings_source,
                file_secret_settings,
            )
