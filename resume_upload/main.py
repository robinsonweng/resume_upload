from __future__ import annotations
import functools
from flask import (
    Flask,
    request,
    session,
    url_for,
)

from apis import api

def create_app() -> Flask:
    app = Flask(__name__)
    # load setting here
    api.init_app(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
