from flask import Blueprint, render_template, abort, request, flash, redirect, url_for

from cache import NewsCache
from models import News, Comments
from forms import CommentForm

news_api = Blueprint("news_api", __name__)


@news_api.route("/", methods=["GET"])
def index():
    # load from redis
    cache_obj = NewsCache()
    news_list = cache_obj.get_index_news()
    # search from mysql
    # news_list = News.query.filter(
    #     News.is_valid == True,
    #     News.is_top == True,
    # ).all()
    return render_template(
        "index.html",
        news_list=news_list,
    )


@news_api.route("/cat/<news_type>", methods=["GET"])
def cat(news_type):
    news_list = News.query.filter(
        News.is_valid == True,
        News.news_type == news_type,
    ).all()
    return render_template(
        "cat.html",
        news_list=news_list,
    )


@news_api.route("/detail/<int:pk>", methods=["GET"])
def detail(pk):
    news_obj = News.query.get(pk)
    form = CommentForm(
        data={
            "object_id": pk,
        }
    )

    if not news_obj or not news_obj.is_valid:
        abort(404)
    return render_template(
        "detail.html",
        news_obj=news_obj,
        form=form,
    )


@news_api.route("/comment/<int:news_id>/add", methods=["POST"])
def comment_add(news_id):
    form = CommentForm(
        data={
            "object_id": news_id,
        }
    )
    news_obj = News.query.get(news_id)
    # submit
    if request.method == "POST":
        if form.validate_on_submit():
            comment_obj = Comments(
                content=form.content.data,
                object_id=news_id,
            )
            print("add comment now: ", comment_obj)
            reply_id = form.reply_id.data
            if reply_id:
                comment_obj.reply_id = reply_id
            comment_obj.save()
            print("added comments")
            flash("comment has been added!", "success")
            return redirect(url_for("news_api.detail", pk=news_id))
        else:
            print("error: ", form.errors)
            flash("invalid input", "danger")

    return render_template(
        "detail.html",
        form=form,
        news_obj=news_obj,
    )
