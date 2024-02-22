from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    List,
    Dict,
)

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from flask_caching import Cache

import os
import base64
import pytest
from urllib.parse import (
    urlparse,
    urljoin,
)

from flask import (
    url_for,
    request,
)

from apis.tus.core import (
    Core,
    CoreFileUpload,
)


class TestTusServerOptions:
    def test_tus_server_options(self, app: Flask, client: FlaskClient):
        with app.app_context():
            url = url_for("files_core")

        response = client.options(url)

        assert response.status_code == 204, response.status_code


class TestTusCreateResource:

    def test_tus_server_post(
        self,
        monkeypatch,
        app: Flask,
        client: FlaskClient,
        flask_cache: Cache,
        filename: str,
        file: bytes,
    ):
        file_id = "24e533e02ec3bc40c387f1a0e460e216"

        monkeypatch.setattr(Core, "generate_file_id", lambda *_: file_id)

        with app.app_context():
            url = url_for("files_core")
            resource_path = url_for("files_core_file_upload", file_id=file_id)

        with app.test_request_context():
            base_url = request.base_url

        based_filename = base64.b64encode(filename.encode()).decode()
        file_metadata = f"filename {based_filename}"
        file_length = len(file)

        headers = {
            "Upload-Length": file_length,
            "Upload-Metadata": file_metadata,
        }

        response = client.post(url, headers=headers)

        resource_url = urljoin(base_url, resource_path)

        expected_header = {
            "Location": resource_url,
            "Tus-Resumable": "1.0.0",
        }

        assert response.status_code == 201, response.status_code
        assert set(expected_header.items()).issubset(set(response.headers.items()))

        raw_upload_url = response.headers["Location"]
        upload_url = urlparse(raw_upload_url)

        file_id = upload_url.path.split('/')[-1]

        cached_resource = flask_cache.get(file_id)

        assert cached_resource["file"] == '\0', cached_resource["file"]
        assert cached_resource["file_metadata"] == file_metadata, cached_resource["file_metadata"]
        assert cached_resource["file_length"] == file_length, cached_resource["file_length"]


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
