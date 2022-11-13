from flask import Flask, abort, json, request, g, Response
from werkzeug.exceptions import HTTPException
from utils.utils import require_appkey, login_required, admin_login_required

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

# api response
app.response_class = CustomResponse

# error handler
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


# capture api logging
@app.before_request
def before_request_func():
    g.method = request.method
    g.url = request.url
    print("!!!!!!!! before_request_func")
    print("!!!!!!!!", request.method)
    print("!!!!!!!!", request.url)


@app.after_request
def after_request_func(response: Response):
    g.status = response.status
    # logger.info(f"method: {g.method}\n url: {g.url}\n status: {g.status}")
    print("+++++++ after_request_func")
    print("+++++++", response.status)
    print("+++++++", response)
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


@app.route("/users", methods=["GET", "POST"])
@require_appkey
@login_required
@admin_login_required
def hello():
    return {
        "status": 200,
        "message": "custom_message",
        "error": "error_message",
        "trace": "trace_message",
        "data": "input_data",
    }
