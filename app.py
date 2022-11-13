import json
from flask import Flask, abort, json, request, g, Response, jsonify
from werkzeug.exceptions import HTTPException
from utils.utils import require_appkey, login_required, admin_login_required

# services
from services.log_service import LogService

# databases
from models.models import db, mongodb

# routes
from routes.news import news_api
from routes.admin import admin_api

# common
from common.response import CustomResponse

# init app
app = Flask(__name__)
app.config.from_object("config.Config")
# mongodb
mongodb.init_app(app=app)
# mysql
db.init_app(app=app)

# routes
app.register_blueprint(news_api)
app.register_blueprint(admin_api)

# api response handle class
app.response_class = CustomResponse

# api error handler
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "error": {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        }
    )
    print(response.data)
    response.content_type = "application/json"
    return response


# capture api logging to mongodb
@app.before_request
def before_request_func():
    method = request.method
    url = request.url
    headers_content = request.headers
    request_content = request.args.to_dict()
    if method != "GET":
        if "multipart/form-data" in headers_content["Content-Type"]:
            request_content = request.form.to_dict()
        else:
            request_content = request.json

    log_service = LogService()
    log_res = log_service.add_one(
        method,
        url,
        ";".join(str(a) for a in headers_content.values()),
        json.dumps(request_content),
    )
    g.method = method
    g.url = url
    g.log_id = log_res["log_id"]


@app.after_request
def after_request_func(response: Response):
    status_code = response.status
    g.status = status_code
    log_service = LogService()
    log_service.update_one(
        g.log_id,
        json.dumps(response.get_json()),
        status_code,
    )
    return response


# @app.route("/migrate_table", methods=["GET"])
# def migrate_table():
#     db.create_all()
#     return {"msg": "ok"}


@app.route("/test1")
def test1():
    abort(409)


@app.route("/test2")
def test2():
    abort(400, "I'm not in the mood to talk!")


@app.route("/hello", methods=["GET", "POST"])
@require_appkey
def hello():
    return {
        "status": 200,
        "message": "custom_message",
        "error": "error_message",
        "trace": "trace_message",
        "data": "input_data",
    }


@app.route("/test_decorator", methods=["GET", "POST"])
@require_appkey
@login_required
@admin_login_required
def test_decorator():
    return {"message": "ok"}


@app.route("/users", methods=["GET", "POST", "PATCH", "PUT", "DELETE"])
def users():
    return {"message": "ok"}
