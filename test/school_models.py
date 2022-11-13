# 1. Column:
# name
# type_
# primary_key
# autoincrement
# comment
# nullable
# default
# unique

# 2. DataType:
# SmallInteger
# Integer
# BigInteger
# Float
# Numeric
# String
# Text
# Date
# Time
# DateTime
# Boolean -> tinyint
# Enum
# PickleType -> BLOB
# LargeBinary -> BLOB
# Interval -> Datetime
# Unicode -> varchar
# UnicodeText -> text
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Enum,
    Boolean,
    SmallInteger,
    ForeignKey,
    text,
)
from sqlalchemy.types import CHAR
from sqlalchemy.dialects.mysql import TINYINT
from enum import IntEnum
from datetime import datetime

#
Base = declarative_base()


class SexEnum(IntEnum):
    MALE = 1
    FEMALE = 0
    UNISEX = 2


"""
  user = User()
  user.addresses
  user.profile
"""


class Student(Base):
    __tablename__ = "students"
    id = Column("id", Integer, primary_key=True)
    stu_no = Column(Integer, nullable=False, unique=True)
    stu_name = Column(String(32), nullable=False)
    sex = Column(Enum(SexEnum), server_default="FEMALE")
    age = Column(SmallInteger, server_default="0", default=0)
    class_name = Column(String(32), nullable=False)
    address = Column(String(255), nullable=False)
    phone_no = Column(CHAR(10), nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.now(),
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        default=None,
    )
    is_valid = Column(Boolean, server_default="1", default=True)

    def __repr__(self):
        return "{} => {}".format(self.stu_no, self.stu_name)


class Course(Base):
    __tablename__ = "courses"
    id = Column("id", Integer, primary_key=True)
    course_name = Column(String(32), nullable=False)
    teacher = Column(String(32), nullable=False)
    desc = Column(String(512))
    created_at = Column(
        DateTime,
        default=datetime.now(),
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        default=None,
    )
    is_valid = Column(Boolean, server_default="1", default=True)

    def __repr__(self):
        return "course: {}".format(self.course_name)


class StudentCourseGrade(Base):
    __tablename__ = "student_course_grades"
    id = Column("id", Integer, primary_key=True)
    score = Column(SmallInteger, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.now(),
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        default=None,
    )

    student_id = Column(
        Integer,
        ForeignKey(Student.id, ondelete="CASCADE"),
        nullable=False,
    )
    course_id = Column(
        Integer,
        ForeignKey(Course.id),
        nullable=False,
    )

    student = relationship(
        "Student",
        backref=backref(
            "grade_list",
            lazy="dynamic",
            cascade="all, delete",
        ),
    )
    # student = relationship(Student, backref="grade_list")

    course = relationship(
        "Course",
        backref=backref(
            "grade_list",
            lazy="dynamic",
        ),
    )
    # course = relationship(Course, backref="grade_list")

    def __repr__(self):
        return "{}-{}: {}".format(
            self.student.stu_name,
            self.course.course_name,
            self.score,
        )
