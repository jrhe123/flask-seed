from flask import Response, jsonify


class CustomResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(CustomResponse, cls).force_type(rv, environ)
