from flask import Flask
from flask_restx import Api

from .tus import (
    tus,
    cache as tus_cache
)


def init_restx() -> Api:
    api = Api(prefix="/api/v1", doc="/api/v1/swagger")

    api.add_namespace(tus)

    return api


def init_app():
    app = Flask(__name__)
    # load setting here

    with app.app_context():
        # waring! order matter here
        # init cache
        tus_cache.init_app(app, config={
            "CACHE_TYPE": "SimpleCache"
        })

        # init restx
        api = init_restx()
        api.init_app(app)

        return app
