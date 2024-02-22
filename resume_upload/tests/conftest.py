from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Generator,
)

if TYPE_CHECKING:
    from flask import Flask

import pytest
from main import create_app

@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app: Flask):
    return app.test_client()


@pytest.fixture()
def runner(app: Flask):
    return app.test_cli_runner()
