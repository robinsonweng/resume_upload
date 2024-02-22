from flask_restx import (
    Resource,
    Namespace,
)
from flask import (
    Response,
    request,
)
from flask_caching import (
    Cache
)

from http import client as status


tus = Namespace("files", path="/files", description="tus protocol")

cache = Cache()

@tus.route("/")
class Core(Resource):
    def options(self):
        return Response(status=status.NO_CONTENT)

    def post(self):
        headers = {
            "Location": "https://tus.example.org/files/24e533e02ec3bc40c387f1a0e460e216",
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
