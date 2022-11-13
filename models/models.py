from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from mongoengine.fields import (
    IntField,
    StringField,
    BooleanField,
    ObjectIdField,
    DateTimeField,
)

# mongodb
mongodb = MongoEngine()

# mysql
db = SQLAlchemy()

# ORM - mysql
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

    def get_comments(self):
        query_set = (
            Comments.objects.filter(
                object_id=self.id,
                is_valid=True,
            )
            .skip(0)
            .limit(10)
        )
        return query_set

    # redis cache: DateTime cannot convert to json
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "img_url": self.img_url,
            "content": self.content,
            "news_type": self.news_type,
            "created_at": self.created_at.strftime(f"%Y-%m-%d"),
        }


# ODM - mongodb
class Comments(mongodb.Document):
    object_id = IntField(required=True, verbose_name="news id")
    content = StringField(required=True, max_length=2000)
    is_valid = BooleanField(default=True)
    reply_id = ObjectIdField()
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    meta = {
        "collection": "comments",
        "ordering": ["-is_valid", "-created_at"],
    }

    @property
    def news_obj(self):
        return News.query.get(self.object_id)

    def __str__(self):
        return f"Comments: {self.content}"


class Log(mongodb.Document):
    object_id = IntField(required=True, verbose_name="log id")
    method = StringField(required=True, max_length=10)
    url = StringField(required=True, max_length=255)
    headers = StringField()
    request = StringField()
    response = StringField()
    status_code = IntField()
    elapse_time = IntField()
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    meta = {
        "collection": "logs",
        "ordering": ["-created_at"],
    }

    def __str__(self):
        return f"Logs: {self.object_id}"
