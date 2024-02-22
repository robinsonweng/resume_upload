from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    List,
    Dict,
)

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient

import pytest

from flask import (
    url_for
)


class TestTusServerOptions:
    def test_tus_server_options(self, app: Flask, client: FlaskClient):
        with app.app_context():
            url = url_for("files_core")

        response = client.options(url)

        assert response.status_code == 204, response.status_code


class TestTusCreateResource:
    def test_tus_server_post(self, app: Flask, client: FlaskClient):
        with app.app_context():
            url = url_for("files_core")

        response = client.post(url)

        expected_header = {
            "Location": "https://tus.example.org/files/24e533e02ec3bc40c387f1a0e460e216",
            "Tus-Resumable": "1.0.0",
        }

        assert response.status_code == 201, response.status_code
        assert set(expected_header.items()).issubset(set(response.headers.items()))


class TestTusCheckFileInfo:
    def test_tus_core_head(self, app: Flask, client: FlaskClient):
        file_id = "24e533e02ec3bc40c387f1a0e460e216"
        with app.app_context():
            url = url_for("files_core_file_upload", file_id=file_id)

        response = client.head(url)

        expected_header = {
            "Upload-Offset": "70",
            "Tus-Resumable": "1.0.0",
        }

        assert response.status_code == 200, response.status_code
        assert set(expected_header.items()).issubset(set(response.headers.items()))
        # ^ check if these header in the reponse headers

class TestTusUploadFile:
    def test_tus_core_patch(self, app: Flask, client: FlaskClient):
        file_id = "24e533e02ec3bc40c387f1a0e460e216"
        with app.app_context():
            url = url_for("files_core_file_upload", file_id=file_id)

        response = client.patch(url)

        expected_header = {
            "Content-Type": "application/offset+octet-stream",
            "Upload-Offset": "70",
            "Tus-Resumable": "1.0.0",
        }

        assert response.status_code == 204, response.status_code
        assert set(expected_header.items()).issubset(set(response.headers.items()))
