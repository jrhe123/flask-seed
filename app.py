from flask import Flask, render_template, abort, redirect, flash, request, url_for
from datetime import datetime

from cache import NewsCache
from forms import NewsForm, CommentForm
from models import db, mongodb, News, Comments

# init app
app = Flask(__name__)
app.config.from_object("config.Config")
# mongodb
mongodb.init_app(app=app)
# mysql
db.init_app(app=app)


@app.route("/migrate_table", methods=["GET"])
def migrate_table():
    db.create_all()
    return {"msg": "ok"}


@app.route("/", methods=["GET"])
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


@app.route("/cat/<news_type>", methods=["GET"])
def cat(news_type):
    news_list = News.query.filter(
        News.is_valid == True,
        News.news_type == news_type,
    ).all()
    return render_template(
        "cat.html",
        news_list=news_list,
    )


@app.route("/detail/<int:pk>", methods=["GET"])
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


@app.route("/admin/", methods=["GET"])
@app.route("/admin/<int:page>", methods=["GET"])
def admin(page=1):
    # page_size = 3
    # page_data = (
    #     News.query.filter(
    #         News.is_valid == True,
    #     )
    #     .limit(page_size)
    #     .offset((page - 1) * page_size)
    # )

    title = request.args.get("title", "")
    page_data = News.query.filter_by(
        is_valid=True,
    )

    if title:
        page_data = page_data.filter(News.title.contains(title))

    page_data = page_data.paginate(
        page=page,
        per_page=3,
    )
    # print(page_data.items)

    return render_template(
        "admin/index.html",
        page_data=page_data,
        title=title,
    )


@app.route("/admin/news/add", methods=["GET", "POST"])
def news_add():
    form = NewsForm()

    # submit
    if request.method == "POST":
        if form.validate_on_submit():
            news_obj = News(
                title=form.title.data,
                content=form.content.data,
                img_url=form.img_url.data,
                news_type=form.news_type.data,
                is_top=form.is_top.data,
            )
            db.session.add(news_obj)
            db.session.commit()

            print("!!!!!!! saved news: ", news_obj)
            # if new added news is on top, then cache in redis
            if news_obj.is_top:
                cache_obj = NewsCache()
                cache_obj.set_index_news()

            print("added news")
            flash("news has been added!", "success")
            return redirect("/admin")
        else:
            print("error: ", form.errors)
            flash("invalid input", "danger")

    return render_template(
        "admin/add.html",
        form=form,
    )


@app.route("/admin/news/update/<int:pk>", methods=["GET", "POST"])
def news_update(pk):
    news_obj = News.query.get(pk)
    if not news_obj.is_valid:
        abort(404)
    form = NewsForm(obj=news_obj)

    # submit
    if request.method == "POST":
        if form.validate_on_submit():

            is_top_origin = news_obj.is_top
            is_top = form.is_top.data

            news_obj.title = form.title.data
            news_obj.content = form.content.data
            news_obj.img_url = form.img_url.data
            news_obj.news_type = form.news_type.data
            news_obj.is_top = is_top
            news_obj.updated_at = datetime.now()
            db.session.add(news_obj)
            db.session.commit()

            # is_top is updated, needs to update cache
            if is_top_origin != is_top:
                cache_obj = NewsCache()
                cache_obj.set_index_news()

            print("updated news")
            flash("news has been updated!", "success")
            return redirect("/admin")
        else:
            print("error: ", form.errors)
            flash("invalid input", "danger")

    return render_template(
        "admin/update.html",
        form=form,
    )


@app.route("/admin/news/delete/<int:pk>", methods=["POST"])
def news_delete(pk):
    if request.method == "POST":
        news_obj = News.query.get(pk)
        if news_obj is None:
            return "no"
        if not news_obj.is_valid:
            return "no"
        news_obj.is_valid = False
        print("now delete news!!")
        db.session.add(news_obj)
        db.session.commit()

        # is_top, needs to update cache
        if news_obj.is_top:
            cache_obj = NewsCache()
            cache_obj.set_index_news()

        return "yes"
    else:
        return "no"


@app.route("/comment/<int:news_id>/add", methods=["POST"])
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
            return redirect(url_for("detail", pk=news_id))
        else:
            print("error: ", form.errors)
            flash("invalid input", "danger")

    return render_template(
        "detail.html",
        form=form,
        news_obj=news_obj,
    )


@app.route("/admin/comment/", methods=["GET"])
@app.route("/admin/comment/<int:page>", methods=["GET"])
def admin_comments(page=1):
    page_data = Comments.objects.all()
    page_data = page_data.paginate(
        page=page,
        per_page=3,
    )
    return render_template(
        "admin/comments.html",
        page_data=page_data,
    )


@app.route("/admin/comment/delete/<string:pk>", methods=["POST"])
def comment_delete(pk):
    if request.method == "POST":
        comment_obj = Comments.objects.filter(id=pk).first()
        if comment_obj is None:
            return "no"
        if not comment_obj.is_valid:
            return "no"
        comment_obj.is_valid = False
        print("now delete comment!!")
        comment_obj.save()
        return "yes"
    else:
        return "no"
