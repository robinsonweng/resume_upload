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
        # check header from user

        try:
            filelength = int(request.headers.get("Upload-Length"))
        except ValueError:
            return Response(status=status.BAD_REQUEST)

        file_metadata = request.headers.get("Upload-Metadata")

        file_id = self.generate_file_id()

        resuorce_path = url_for("files_core_file_upload", file_id=file_id)
        resource_url = urljoin(request.base_url, resuorce_path)

        resource= {
            "file": '\0',
            "file_metadata": file_metadata,
            "file_length": filelength,
        }
        cache.set(file_id, resource)

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
