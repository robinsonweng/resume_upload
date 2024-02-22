from flask_restx import Api

from .tus.core import tus

api = Api(prefix="/api/v1", doc="/api/v1/swagger")

api.add_namespace(tus)
