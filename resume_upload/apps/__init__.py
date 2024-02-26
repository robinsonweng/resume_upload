from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

if TYPE_CHECKING:
    pass

from pathlib import Path
from flask import Flask, current_app
from flask_restx import Api

from .tus import (
    tus,
    cache as tus_cache
)

from configs import (
    ProductionConfig,
    DevelopmentConfig,
)


def init_restx() -> Api:
    api = Api(prefix="/api/v1", doc="/api/v1/swagger")

    api.add_namespace(tus)

    return api


def init_app():
    app = Flask(__name__)
    # load setting here
    work_dir = Path(app.root_path).parent.parent
    if app.debug is True:
        dev_config = DevelopmentConfig(work_dir)
        app.config.from_object(dev_config)
    else:
        prod_config = ProductionConfig(work_dir)
        app.config.from_object(prod_config)

    with app.app_context():
        # warning! order matters here
        # init cache
        tus_cache.init_app(app, config={
            "CACHE_TYPE": current_app.config["TUS_CACHE_TYPE"]
        })

        # init restx
        api = init_restx()
        api.init_app(app)

        return app
