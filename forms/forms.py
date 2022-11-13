from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
    DateField,
    BooleanField,
    HiddenField,
)
from wtforms.validators import DataRequired, Length, ValidationError


def validate_content(form, field):
    value = field.data
    if len(value) <= 50:
        raise ValidationError("content is less than 50 characters")
    return field


NEWS_TYPE_CHOICES = (
    ("local", "local"),
    ("global", "global"),
    ("miltary", "miltary"),
    ("entertainment", "entertainment"),
)


class NewsForm(FlaskForm):
    title = StringField(
        label="title",
        validators=[
            DataRequired("title"),
            Length(min=20, max=200, message="title must be 20 - 200 characters"),
        ],
        description="title",
        render_kw={"class": "form-control"},
    )
    content = TextAreaField(
        label="content",
        validators=[DataRequired("content"), validate_content],
        description="content",
        render_kw={"class": "form-control", "rows": 5},
    )
    news_type = SelectField(
        "news_type",
        choices=NEWS_TYPE_CHOICES,
        render_kw={"class": "form-control"},
    )
    img_url = StringField(
        label="image",
        description="image",
        default="/static/img/news/new1.jpg",
        render_kw={"required": "required", "class": "form-control"},
    )
    is_top = BooleanField(label="top")
    submit = SubmitField(label="submit", render_kw={"class": "btn btn-info"})


class CommentForm(FlaskForm):
    object_id = HiddenField(
        label="news id",
        validators=[
            DataRequired("news id"),
        ],
    )
    reply_id = HiddenField(
        label="reply id",
    )
    content = TextAreaField(
        label="content",
        validators=[
            DataRequired("content"),
            Length(
                min=5,
                max=200,
                message="content must be 5-200characters",
            ),
        ],
        description="content",
        render_kw={"class": "form-control", "rows": 5},
    )
    submit = SubmitField(label="submit", render_kw={"class": "btn btn-info"})
