from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Union,
)

if TYPE_CHECKING:
    pass

import os
from pathlib import Path
import tomllib


CONFIG_FILE_NAME = "config.toml"


class Config(object):
    def __init__(self, work_dir: Union[Path, str]) -> None:
        path = os.path.join(work_dir, CONFIG_FILE_NAME)
        with open(path, "rb") as f:
            self.file = tomllib.load(f)

    def __getattr__(self, value):
        return self.file[value]

    TESTING = False


class ProductionConfig(Config):
    TUS_CACHE_TYPE = "SimpleCache"


class DevelopmentConfig(Config):
    TUS_CACHE_TYPE = "SimpleCache"


class TestConfig(object):
    TESTING = True
    SERVER_NAME = "localhost"
    TUS_CACHE_TYPE = "SimpleCache"
