import re
from mongoengine import Document, connect, EmbeddedDocument
from mongoengine.fields import (
    IntField,
    StringField,
    EnumField,
    ListField,
    EmbeddedDocumentField,
)
from mongoengine.errors import ValidationError
from enum import Enum


connect("flask_seed", username="root", password="root", authentication_source="admin")


class SexChoices(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


def phone_required(value):
    pattern = r"^[0-9]{10}$"
    if not re.search(pattern, value):
        raise ValidationError("invalid phone number")


class CourseGrade(EmbeddedDocument):
    course_name = StringField(max_length=64, required=True)
    teacher = StringField(max_length=16)
    score = IntField(required=True, min_value=0, max_value=100)


class Student(Document):
    stu_no = IntField(required=True, unique=True)
    stu_name = StringField(required=True, max_length=16)
    sex = EnumField(enum=SexChoices)
    class_name = StringField(max_length=10)
    address = StringField(max_length=255)
    # phone_no = StringField(max_length=10)
    phone_no = StringField(validation=phone_required)
    age = IntField(min_value=0, max_value=1000)

    # grades: [12,3,4,5]
    # grades = ListField(IntField())

    # grades: [{"score": 80}, {"score": 90}]
    grades = ListField(EmbeddedDocumentField(CourseGrade))

    # grade: {"score": 80}
    # grade = EmbeddedDocumentField(CourseGrade)

    meta = {
        "collection": "students",
        "ordering": ["-age"],
    }

    def __str__(self):
        return f"{self.stu_no}: {self.stu_name}"


class StudentGrade(Document):
    stu_no = IntField(required=True)
    stu_name = StringField(required=True, max_length=16)
    sex = EnumField(enum=SexChoices)
    class_name = StringField(max_length=10)
    address = StringField(max_length=255)
    phone_no = StringField(max_length=10)
    age = IntField(min_value=0, max_value=1000)

    # grades: [12,3,4,5]
    # grades = ListField(IntField())

    # grades: [{"score": 80}, {"score": 90}]
    # grades = ListField(EmbeddedDocumentField(CourseGrade))

    # grade: {"score": 80}
    grade = EmbeddedDocumentField(CourseGrade)

    meta = {
        "collection": "grades",
        "ordering": ["-stu_no"],
    }

    def __str__(self):
        return f"{self.stu_no}: {self.stu_name}"
