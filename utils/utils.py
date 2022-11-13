from flask import abort, request, current_app, g, jsonify
from functools import wraps
import jwt


# 1. api key example
def require_appkey(f):
    @wraps(f)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if (
            request.headers.get("api-key")
            and request.headers.get("api-key") == current_app.config["API_KEY"]
        ):
            return f(*args, **kwargs)
        else:
            abort(401, "api key is required")

    return decorated_function


# 2. token example
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        if not request.headers.get("Authorization"):
            return abort(401, "token is required")
        # get user via some ORM system
        # user = User.get(request.headers["authorization"])
        user = {
            "is_admin": True,
        }
        # make user available down the pipeline via flask.g
        g.user = user
        # finally call f. f() now haves access to g.user
        """OR: we can pass user as return as well"""
        # return f(user, *args, **kwargs)
        return f(*args, **kwargs)

    return wrap


def admin_login_required(f):
    def wrap(*args, **kwargs):
        # user is available from @login_required
        if not g.user["is_admin"]:
            abort(401, "user role is invalid")
        return f(*args, **kwargs)

    return wrap


# 3. jwt example
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"])
            # current_user = User.query.filter_by(public_id=data["public_id"]).first()
            current_user = {
                "guid": "1001",
                "username": "roytest",
            }
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated
