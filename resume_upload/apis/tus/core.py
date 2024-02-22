import os
import base64

from flask_restx import (
    Resource,
    Namespace,
)
from flask import (
    Response,
    request,
    url_for,
)
from flask_caching import (
    Cache
)

from http import client as status
from urllib.parse import (
    urlparse,
    urljoin
)



tus = Namespace("files", path="/files", description="tus protocol")

cache = Cache()

@tus.route("/")
class Core(Resource):
    def options(self):
        return Response(status=status.NO_CONTENT)

    @staticmethod
    def generate_file_id():
        return str(base64.urlsafe_b64encode(os.urandom(32))).replace('=', '')

    def post(self):
        file_id = self.generate_file_id()

        cache.set(file_id, '\0')

        resuorce_path = url_for("files_core_file_upload", file_id=file_id)
        resource_url = urljoin(request.base_url, resuorce_path)

        headers = {
            "Location": resource_url,
            "Tus-Resumable": "1.0.0",
        }

        return Response(
            status=status.CREATED,
            headers=headers,
        )


@tus.route("/<string:file_id>")
class CoreFileUpload(Resource):
    """
        core protocol:
        - HEAD
        - PATCH
        - OPTIONS
    """
    def head(self, file_id):
        # check header
        tus_version = request.headers.get("Tus-Reusmable")

        headers = {
            "Upload-Offset": "70",
            "Tus-Resumable": "1.0.0",
        }
        return Response(
            status=status.OK,
            headers=headers,
        )

    def patch(self, file_id):
        headers = {
            "Content-Type": "application/offset+octet-stream",
            "Upload-Offset": "70",
            "Tus-Resumable": "1.0.0",
        }

        return Response(
            status=status.NO_CONTENT,
            headers=headers,
        )
