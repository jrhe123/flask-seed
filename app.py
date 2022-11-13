from flask import (
    Flask,
    abort,
    json,
)
from werkzeug.exceptions import HTTPException

from models import db, mongodb

from routes.news import news_api
from routes.admin import admin_api

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


@app.route("/migrate_table", methods=["GET"])
def migrate_table():
    db.create_all()
    return {"msg": "ok"}


@app.route("/test1")
def test1():
    abort(409)


@app.route("/test2")
def test2():
    abort(400, "I'm not in the mood to talk!")
