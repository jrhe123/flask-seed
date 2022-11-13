from flask import (
    render_template,
    abort,
    redirect,
    flash,
    request,
    Blueprint,
)
from datetime import datetime

from redis_cache import NewsCache
from forms.forms import NewsForm
from models.models import db, News, Comments

admin_api = Blueprint("admin_api", __name__)


@admin_api.route("/admin/", methods=["GET"])
@admin_api.route("/admin/<int:page>", methods=["GET"])
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

    return render_template(
        "admin/index.html",
        page_data=page_data,
        title=title,
    )


@admin_api.route("/admin/news/add", methods=["GET", "POST"])
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


@admin_api.route("/admin/news/update/<int:pk>", methods=["GET", "POST"])
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


@admin_api.route("/admin/news/delete/<int:pk>", methods=["POST"])
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


@admin_api.route("/admin/comment/", methods=["GET"])
@admin_api.route("/admin/comment/<int:page>", methods=["GET"])
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


@admin_api.route("/admin/comment/delete/<string:pk>", methods=["POST"])
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
