from __future__ import annotations
from typing import (
    TYPE_CHECKING
)

if TYPE_CHECKING:
    pass

from flask import (
    Flask,
)

from apis import (
    api,
)
from apis.tus.core import (
    cache,
)


def create_app() -> Flask:
    app = Flask(__name__)
    # load setting here
    api.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
