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
    urljoin
)


tus = Namespace("files", path="/files", description="tus protocol")

cache = Cache()


@tus.route("/")
class Core(Resource):
    def options(self):
        headers = {
            "Tus-Resumable": "1.0.0",
            "Tus-Version": "1.0.0",
            "Tus-Max-Size": "1073741824",
            "Tus-Extension": "creation,expiration",
        }

        return Response(
            status=status.NO_CONTENT,
            headers=headers,
        )

    def post(self):
        try:
            file_length = int(request.headers.get("Upload-Length"))
        except ValueError:
            return Response(status=status.BAD_REQUEST)

        file_metadata = request.headers.get("Upload-Metadata")

        file_id = self.generate_file_id()

        resuorce_path = url_for("files_core_file_upload", file_id=file_id)
        resource_url = urljoin(request.base_url, resuorce_path)

        resource = {
            "file": '\0',
            "file_metadata": file_metadata,
            "file_length": file_length,
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

    @staticmethod
    def generate_file_id():
        return str(base64.urlsafe_b64encode(os.urandom(32))).replace('=', '')


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

        cached_resource = cache.get(file_id)  # no sanatize?

        if cached_resource is None:
            headers = {
                "Tus-Resumable": "1.0.0"
            }
            return Response(
                status=status.NOT_FOUND,
                headers=headers,
            )

        cached_length = len(cached_resource["file"])

        headers = {
            "Upload-Offset": cached_length,
            "Tus-Resumable": "1.0.0",
        }
        return Response(
            status=status.OK,
            headers=headers,
        )

    def patch(self, file_id):
        resource = cache.get(file_id)
        if resource is None:
            headers = {
                "Tus-Resumable": "1.0.0",
            }
            return Response(
                status=status.NOT_FOUND,
                headers=headers
            )

        try:
            offset = int(request.headers.get("Upload-Offset"))
        except ValueError:
            headers = {
                "Tus-Resumable": "1.0.0",
            }
            return Response(
                status=status.BAD_REQUEST,
                headers=headers,
            )

        content_type = request.headers.get("Content-Type")
        if content_type != "application/offset+octet-stream":
            headers = {
                "Tus-Resumable": "1.0.0",
            }
            return Response(
                status=status.UNSUPPORTED_MEDIA_TYPE,
                headers=headers,
            )

        try:
            int(request.headers.get("Content-Length"))
        except ValueError:
            headers = {
                "Tus-Resumable": "1.0.0",
            }
            return Response(
                status=status.BAD_REQUEST,
                headers=headers,
            )

        file_chunk = request.data
        chunk_length = len(file_chunk)
        updated_offset = offset + chunk_length

        file = resource["file"]
        resource["file"] = file + file_chunk
        cache.set(file_id, resource)

        headers = {
            "Content-Type": "application/offset+octet-stream",
            "Upload-Offset": updated_offset,
            "Tus-Resumable": "1.0.0",
        }
        return Response(
            status=status.NO_CONTENT,
            headers=headers,
        )
