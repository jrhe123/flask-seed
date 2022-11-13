import redis, json
from flask import current_app
from datetime import datetime

from models import News


class BaseRedisConnection(object):
    def __init__(self):
        redis_config = current_app.config["REDIS_SETTINGS"]
        pool = redis.ConnectionPool(**redis_config)
        connection = redis.Redis(
            connection_pool=pool,
        )
        self.connection = connection

    def __del__(self):
        try:
            print("destory now")
            self.connection.close()
        except Exception as e:
            print(e)

    def delete(self, key):
        self.connection.delete(key)


class NewsCache(BaseRedisConnection):
    def set_index_news(self):
        query_set = (
            News.query.filter(
                News.is_valid == True,
                News.is_top == True,
            )
            .order_by(News.updated_at.desc())
            .all()
        )

        news_list = []
        for item in query_set:
            news_list.append(item.to_dict())

        key = current_app.config["INDEX_NEWS_KEY"]
        data = {
            key: news_list,
            "t": datetime.now().timestamp(),  # for debug
        }
        result = self.connection.set(key, json.dumps(data))
        print("cached now!!! ", result)

    def get_index_news(self):

        key = current_app.config["INDEX_NEWS_KEY"]
        result = self.connection.get(key)
        if result is None:
            self.set_index_news()
            result = self.connection.get(key)

        news_info = json.loads(result)
        print("load from cache!!!")
        return news_info[key]
