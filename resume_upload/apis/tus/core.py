from flask_restx import (
    Resource,
    Namespace,
)
from flask import (
    Response,
    request,
)

from http import client as status

tus = Namespace("files", path="/files", description="tus protocol")


@tus.route("/")
class Core(Resource):
    def options(self):
        return Response(status=status.NO_CONTENT)


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
