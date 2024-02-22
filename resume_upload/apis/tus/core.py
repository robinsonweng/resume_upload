from flask_restx import (
    Resource,
    Namespace,
)

tus = Namespace("files", path="/files", description="tus protocol")

@tus.route("/")
class HelloWorld(Resource):
    def get(self):
        return {"status":"wellcome to the name space"}

