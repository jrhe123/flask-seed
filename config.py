import os


class Config(object):
    # form required
    # csrf - in jinja template required
    SECRET_KEY = "123123"
    SQLALCHEMY_DATABASE_URI = os.environ.get("MYSQL_DATABASE_URI")
    MONGODB_SETTINGS = {
        "db": "flask_seed",
        "host": "mongo-container",
        "port": 27017,
        "username": "root",
        "password": "root",
    }
    REDIS_SETTINGS = {
        "host": "redis",
        "password": "",
        "port": 6379,
        "db": 1,  # 0-15, choose one of them
        "max_connections": 20,
        "decode_responses": True,  # decode utf-8
    }
    # redis cache key
    INDEX_NEWS_KEY = "INDEX_NEWS_KEY"
    # api key
    API_KEY = os.environ.get("API_KEY")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass
