# coding=utf-8
from os.path import dirname, abspath

from pydantic import BaseModel
import yaml


_BASE_PATH_ = dirname(dirname(abspath(__file__)))


class _NetBox(BaseModel):
    base_url: str
    api_token: str


class _Configuration(BaseModel):
    NetBox: _NetBox

    def __init__(self):
        target_path = f'{_BASE_PATH_}/configuration.yaml'

        try:
            with open(target_path) as file:
                data = list(yaml.safe_load_all(file))[0]

            super().__init__(**data)

        except Exception as e:
            raise ValueError(f'Can\'t load the configuration from: {target_path}') from e


Configuration = _Configuration()
