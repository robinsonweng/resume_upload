from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Generator,
)

if TYPE_CHECKING:
    from flask import Flask
    from flask_caching import Cache

import pytest
from resume_upload.apps import init_app
from resume_upload.apps.tus import cache


@pytest.fixture(scope="class")
def app() -> Generator[Flask, None, None]:
    app = init_app()
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


@pytest.fixture(scope="class")
def flask_cache(app: Flask) -> Cache:
    return cache


@pytest.fixture(scope="class")
def filename() -> str:
    return "test file.txt"


@pytest.fixture(scope="class")
def file() -> bytes:
    return "test file text is not very long".encode()
