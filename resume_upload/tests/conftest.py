from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Generator,
)

if TYPE_CHECKING:
    from flask import Flask
    from flask_caching import Cache

import pytest
from main import create_app
from apis.tus.core import cache


@pytest.fixture(scope="class")
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SERVER_NAME": "localhost",
    })

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture(scope="class")
def client(app: Flask):
    return app.test_client()


@pytest.fixture(scope="class")
def runner(app: Flask):
    return app.test_cli_runner()
