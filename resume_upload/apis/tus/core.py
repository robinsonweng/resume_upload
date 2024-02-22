from flask_restx import (
    Resource,
    Namespace,
)
from flask import (
    make_response,
    Response,
)

from http import client as status

tus = Namespace("files", path="/files", description="tus protocol")


@tus.route("/")
class TusOptions(Resource):
    def options(self):
        return Response(status=status.NO_CONTENT)


@tus.route("/<string:file_id>")
class Core(Resource):
    """
        core protocol:
        - HEAD
        - PATCH
        - OPTIONS
    """
    def head(self, file_id):
        return Response(status=status.OK)

    def patch(self, file_id):
        return Response(status=status.NO_CONTENT)
