from sqlalchemy.orm import Session
from sqlalchemy import select, sql, Table, and_, MetaData

from db_engine import engine_future as engine

# from user_profile_model import UserProfile
# from user_address_model import UserAddress
# from user_model import User
from user_models import User, UserProfile, UserAddress


class MySqlOrmTest(object):
    def join_table(self):
        # init session
        session = Session(bind=engine, future=True)

        user_obj = session.get(User, {"id": 5})
        addr_list = user_obj.addresses
        # dynamic
        filter_list = addr_list.filter(UserAddress.id < 2)

        print(type(addr_list))  # AppenderQuery
        for addr in addr_list:
            print("origin: ", addr)
        for addr in filter_list:
            print("filtered: ", addr)

        session.close()

    def get_user_by_id(self, pk):
        session = Session(bind=engine, future=True)
        user_obj = session.get(User, {"id": pk})
        session.close()
        return user_obj

    def get_one(self):
        session = Session(bind=engine, future=True)
        # stmt = select(User)
        # row = session.execute(stmt).fetchone()
        # row = session.execute(stmt).scalars().first()
        # stmt = stmt.where(User.id == 1)
        # stmt = select([User.username, User.age,]).where(
        #     and_(
        #         User.id == "5",
        #         User.age == 0,
        #     )
        # )
        stmt = select([User]).where(
            and_(
                User.id == "5",
                User.age == 0,
            )
        )
        # row = session.execute(stmt).scalars().one()
        row = session.execute(stmt).scalar_one_or_none()
        session.close()
        return row

    def get_more(self):
        session = Session(bind=engine, future=True)
        stmt = select([User])
        rows = session.execute(stmt)
        return rows, session

    def add_user_and_address(self):
        # init session
        with Session(bind=engine, future=True) as session:
            user_obj = User(
                username="roytest_888",
                password="123456789",
                real_name="jiarong_888",
            )
            profile = UserProfile(
                user=user_obj,
                hobby="play basketball",
            )
            user_obj.addresses.append(
                UserAddress(
                    user=user_obj,
                    area="addr2",
                    phone_no="1234567888",
                    remark="work addr",
                )
            )
            session.begin()
            try:
                session.add(user_obj)
                session.add(profile)
            except:
                session.rollback()
            else:
                session.commit()
                session.close()

    def add_user(self):
        # init session
        session = Session(bind=engine, future=True)

        # 1. add one user
        # # create user obj
        # user_obj = User(
        #     username="roytest",
        #     password="123456",
        #     real_name="jiarong",
        # )
        # # add & commit
        # session.add(user_obj)

        # 2. add multi users
        user_list = []
        for i in range(3):
            user_list.append(
                User(
                    username="roytest_{}".format(i),
                    password="123456",
                    real_name="jiarong_{}".format(i),
                )
            )
        session.add_all(user_list)
        session.commit()
        session.close()


def main():
    obj = MySqlOrmTest()
    # obj.add_user()

    # obj.add_user_and_address()

    # user_obj = obj.get_user_by_id(5)

    # user_obj = obj.get_one()

    # user_obj_list, session = obj.get_more()
    # for user_obj in user_obj_list:
    #     print(user_obj)
    # session.close()

    obj.join_table()


if __name__ == "__main__":
    main()
