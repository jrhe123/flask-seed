from flask import Flask, request, make_response, redirect, abort, render_template
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/flask_seed"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "account_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    is_valid = db.Column(
        db.Boolean,
        default=True,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.now(),
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(),
    )
    news_type = db.Column(
        db.Enum(
            "local",
            "global",
            "entertainment",
            "miltary",
        ),
    )
    is_top = db.Column(
        db.Boolean,
        default=False,
    )


"""
1. url query:
string - default
int
float
path
uuid
"""


@app.route("/migrate_table", methods=["GET"])
def migrate_table():
    db.create_all()
    return {"msg": "ok"}


def index():
    username = "roy test"
    age = 12
    user_obj = {
        "username": "roy test",
        "age": 12,
    }
    city_tuple = ("toronto", "quebec", "vancouver")
    return render_template(
        "index.html",
        username=username,
        age=age,
        user_obj=user_obj,
        city_tuple=city_tuple,
        score=100,
        phone_number="6479291623",
    )


@app.template_filter("phone_format")
def phone_format(phone_number):
    return phone_number[0:3] + "****" + phone_number[7:]


@app.route("/test", methods=["GET"])
def test():
    # response tuple
    # (response, status, headers)
    # (response, headers)
    # 1. response
    # return "123", 201, {"user_id": "123"}
    # return make_response(
    #     "123",
    #     201,
    #     {"user_id": "123"},
    # )
    # 2. redirect
    # return redirect("/")
    # 3. abort
    ip_list = ["127.0.0.1"]
    ip = request.remote_addr
    if ip in ip_list:
        abort(403)
    return "ok"


@app.route("/", methods=["GET"])
def hello_world():
    # 1: headers
    ip = request.remote_addr
    headers = request.headers
    ua = headers.get("user-agent")
    # 2: ?name=roytest&age=12
    query_name = request.args.get("name")
    query_age = request.args.get("age")
    print("query_name: {}".format(query_name))
    print("query_age: {}".format(query_age))
    return ip


@app.route("/user/", methods=["GET"])
@app.route("/user/<username>", methods=["GET"])
def test_2(username=None):
    return "hello world {}".format(username)


@app.route("/post/", methods=["GET"])
@app.route("/post/<int:post_id>", methods=["GET"])
def test_1(post_id=0):
    return "hello world {}".format(post_id)


if __name__ == "__main__":
    app.run()
