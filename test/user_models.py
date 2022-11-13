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


"""
  user = User()
  user.addresses
  user.profile
"""


class SexEnum(IntEnum):
    MALE = 1
    FEMALE = 0
    UNISEX = 2


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(512), nullable=False)
    real_name = Column(String(32))
    sex = Column(Enum(SexEnum), server_default="FEMALE")
    age = Column(SmallInteger, server_default="0", default=0)
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

    # user.profile (one-to-one)
    profile = relationship("UserProfile", backref="user", uselist=False)

    def __repr__(self):
        return "{} => {}".format(self.username, self.real_name)


class UserAddress(Base):
    __tablename__ = "addresses"
    id = Column("id", Integer, primary_key=True)
    area = Column(String(256), nullable=False)
    phone_no = Column(CHAR(10), nullable=False)
    remark = Column(String(512))
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
    # one-to-many: defined in the child table
    user_id = Column(Integer, ForeignKey(User.id))

    # testing
    user = relationship(
        "User",
        backref=backref(
            "addresses",
            lazy="dynamic",
        ),
    )
    # user = relationship(User, backref="addresses")

    def __repr__(self):
        return "{} => {}".format(self.id, self.area)


class UserProfile(Base):
    __tablename__ = "profiles"
    id = Column("id", Integer, primary_key=True)
    hobby = Column(String(255))
    created_at = Column(
        DateTime,
        default=datetime.now(),
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        default=None,
    )
    # one-to-one
    user_id = Column(Integer, ForeignKey(User.id))
    # user = relationship("User", backref=backref("profile", uselist=False))
