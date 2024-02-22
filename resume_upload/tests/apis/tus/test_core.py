from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    List,
    Dict,
)

from flask import (
    url_for
)

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from flask import Flask

def test_tus_server_options(app: Flask, client: FlaskClient):
    with app.app_context():
        url = url_for("files_tus_options")

    response = client.options(url)

    assert response.status_code == 204, response.status_code

def test_tus_core_head(app: Flask, client: FlaskClient):
    with app.app_context():
        url = url_for("files_core", file_id=123)

    response = client.head(url)

    assert response.status_code == 200, response.status_code

def test_tus_core_patch(app: Flask, client: FlaskClient):
    with app.app_context():
        url = url_for("files_core", file_id=123)

    response = client.patch(url)

    assert response.status_code == 204, response.status_code

